# (c) City96 || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import collections
import logging

import torch

import folder_paths
from comfy import ldm, sd, utils, model_patcher, model_management, lora, float
from .dequant import is_quantized, is_torch_compatible
from .loader import gguf_clip_loader, gguf_sd_loader
from .ops import GGMLOps, move_patch_to_device
from ..utils import raise_unless, get_embedding_directory, apply_lora_stack


def attention_override_pytorch(func, *args, **kwargs):
    new_attention = ldm.modules.attention.attention_pytorch

    return new_attention.__wrapped__(*args, **kwargs)


def attention_override_sage(func, *args, **kwargs):
    new_attention = ldm.modules.attention.attention_sage

    return new_attention.__wrapped__(*args, **kwargs)


def attention_override_xformers(func, *args, **kwargs):
    new_attention = ldm.modules.attention.attention_xformers

    return new_attention.__wrapped__(*args, **kwargs)


def attention_override_flash(func, *args, **kwargs):
    new_attention = ldm.modules.attention.attention_flash

    return new_attention.__wrapped__(*args, **kwargs)


ATTENTION_OVERRIDES = {
    "sdpa": attention_override_pytorch,
    "sageattn": attention_override_sage,
    "xformers": attention_override_xformers,
    "flashattn": attention_override_flash,
}


class GGUFModelPatcher(model_patcher.ModelPatcher):
    patch_on_device = False

    def patch_weight_to_device(self, key, device_to=None, inplace_update=False):
        if key not in self.patches:
            return
        weight = utils.get_attr(self.model, key)

        patches = self.patches[key]
        if is_quantized(weight):
            out_weight = weight.to(device_to)
            patches = move_patch_to_device(patches, self.load_device if self.patch_on_device else self.offload_device)
            # TODO: do we ever have legitimate duplicate patches? (i.e. patch on top of patched weight)
            out_weight.patches = [(patches, key)]
        else:
            inplace_update = self.weight_inplace_update or inplace_update
            if key not in self.backup:
                self.backup[key] = collections.namedtuple('Dimension', ['weight', 'inplace_update'])(
                    weight.to(device=self.offload_device, copy=inplace_update), inplace_update
                )

            if device_to is not None:
                temp_weight = model_management.cast_to_device(weight, device_to, torch.float32, copy=True)
            else:
                temp_weight = weight.to(torch.float32, copy=True)

            out_weight = lora.calculate_weight(patches, temp_weight, key)
            out_weight = float.stochastic_rounding(out_weight, weight.dtype)

        if inplace_update:
            utils.copy_to_param(self.model, key, out_weight)
        else:
            utils.set_attr_param(self.model, key, out_weight)

    def unpatch_model(self, device_to=None, unpatch_weights=True):
        if unpatch_weights:
            for p in self.model.parameters():
                if is_torch_compatible(p):
                    continue
                patches = getattr(p, "patches", [])
                if len(patches) > 0:
                    p.patches = []

        # TODO: Find another way to not unload after patches
        return super().unpatch_model(device_to=device_to, unpatch_weights=unpatch_weights)

    def pin_weight_to_device(self, key):
        op_key = key.rsplit('.', 1)[0]
        if not self.mmap_released and op_key in self.named_modules_to_munmap:
            # TODO: possible to OOM, find better way to detach
            self.named_modules_to_munmap[op_key].to(self.load_device).to(self.offload_device)
            del self.named_modules_to_munmap[op_key]
        super().pin_weight_to_device(key)

    mmap_released = False
    named_modules_to_munmap = {}

    def load(self, *args, force_patch_weights=False, **kwargs):
        if not self.mmap_released:
            self.named_modules_to_munmap = dict(self.model.named_modules())

        # always call `patch_weight_to_device` even for lowvram
        super().load(*args, force_patch_weights=True, **kwargs)

        # make sure nothing stays linked to mmap after first load
        if not self.mmap_released:
            linked = []
            if kwargs.get("lowvram_model_memory", 0) > 0:
                for n, m in self.named_modules_to_munmap.items():
                    if hasattr(m, "weight"):
                        device = getattr(m.weight, "device", None)
                        if device == self.offload_device:
                            linked.append((n, m))
                            continue
                    if hasattr(m, "bias"):
                        device = getattr(m.bias, "device", None)
                        if device == self.offload_device:
                            linked.append((n, m))
                            continue
            if linked and self.load_device != self.offload_device:
                logging.info(f"Attempting to release mmap ({len(linked)})")
                for n, m in linked:
                    # TODO: possible to OOM, find better way to detach
                    m.to(self.load_device).to(self.offload_device)
            self.mmap_released = True
            self.named_modules_to_munmap = {}

    def clone(self, *args, **kwargs):
        src_cls = self.__class__
        self.__class__ = GGUFModelPatcher
        n = super().clone(*args, **kwargs)
        n.__class__ = GGUFModelPatcher
        self.__class__ = src_cls
        # GGUF specific clone values below
        n.patch_on_device = getattr(self, "patch_on_device", False)
        n.mmap_released = getattr(self, "mmap_released", False)
        if src_cls != GGUFModelPatcher:
            n.size = 0  # force recalc

        return n


def load_text_encoder_data(text_encoder_paths):
    text_encoder_data = []
    for path in text_encoder_paths:
        if path.endswith(".gguf"):
            state_dict = gguf_clip_loader(path)
        else:
            state_dict = utils.load_torch_file(path, safe_load=True)
            if "scaled_fp8" in state_dict:  # NOTE: Scaled FP8 would require different custom ops, but only one can be active
                raise NotImplementedError(f"Mixing scaled FP8 with GGUF is not supported! Use regular CLIP loader or switch model(s)\n({path})")
        text_encoder_data.append(state_dict)

    return text_encoder_data


def get_dtype(dtype):
    match dtype:
        case None | "default":
            return None
        case "target":
            return dtype
        case _:
            return getattr(torch, dtype)


def load_diffusion_model_gguf(**kwargs):
    ggmlops = GGMLOps()
    ggmlops.Linear.dequant_dtype = get_dtype(kwargs.get("model_dequant_dtype"))
    ggmlops.Linear.patch_dtype = get_dtype(kwargs.get("model_patch_dtype"))

    model_path = folder_paths.get_full_path("diffusion_models_gguf", kwargs.get("diffusion_model"))
    state_dict, extra = gguf_sd_loader(model_path)
    metadata = extra.get("metadata", {})
    model = sd.load_diffusion_model_state_dict(
        state_dict,
        model_options={"custom_operations": ggmlops},
        metadata=metadata
    )
    raise_unless(model, RuntimeError, f"Could not detect model type of: {model_path}")

    patch_on_device, attention_override, enable_fp16_accumulation = False, "None", False
    extended_params = kwargs.get("extended_params")
    if extended_params.get("extended_params") == "Manual":
        patch_on_device = extended_params.get("model_patch_on_device")
        attention_override = extended_params.get("attention_override")

    model = GGUFModelPatcher.clone(model)
    model.patch_on_device = patch_on_device

    if attention_override != "None":
        model.model_options["transformer_options"]["optimized_attention_override"] = ATTENTION_OVERRIDES["attention_override"]

    if hasattr(torch.backends.cuda.matmul, "allow_fp16_accumulation"):
        torch.backends.cuda.matmul.allow_fp16_accumulation = enable_fp16_accumulation
    else:
        logging.warning("allow_fp16_accumulation not supported in this PyTorch version, skipping")

    return model


def load_text_encoders_gguf(clip_type, **kwargs):
    paths = [
        folder_paths.get_full_path("text_encoders_gguf", kwargs.get("text_encoder")),
        folder_paths.get_full_path("text_encoders_gguf", kwargs.get("embeddings_connector")),
    ]

    load_device = model_management.text_encoder_device()
    offload_device = model_management.text_encoder_offload_device()

    extended_params = kwargs.get("extended_params")
    if extended_params.get("extended_params") == "Manual":
        if extended_params.get("text_encoder_device") == "cpu":
            load_device = torch.device("cpu")

    text_encoder_data = load_text_encoder_data(paths)

    model_options = {
        "custom_operations": GGMLOps(),
        "load_device": load_device,
        "offload_device": offload_device,
    }
    text_encoder = sd.load_text_encoder_state_dicts(
        clip_type=clip_type,
        state_dicts=text_encoder_data,
        model_options=model_options,
        embedding_directory=get_embedding_directory(),
    )
    text_encoder.patcher = GGUFModelPatcher.clone(text_encoder.patcher)

    return text_encoder
