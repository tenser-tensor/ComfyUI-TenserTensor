# Contains slightly modified code by City96
# (c) City96 || Apache-2.0 (apache.org/licenses/LICENSE-2.0)
# Modified by TenserTensor
# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import collections as C
import inspect as I
import logging as LOG

import folder_paths as FP
import torch
from comfy import float as FL, lora as L, model_management as MM, model_patcher as MP, sd as SD, utils as U

from ...gguf.dequant import is_quantized, is_torch_compatible
from ...gguf.loader import gguf_sd_loader, gguf_clip_loader
from ...gguf.ops import GGMLOps, move_patch_to_device

WeightBackup = C.namedtuple('WeightBackup', ['weight', 'inplace_update'])


class GGUFModelPatcher(MP.ModelPatcher):
    patch_on_device = False

    def patch_weight_to_device(self, key, device_to=None, inplace_update=False):
        if key not in self.patches:
            return

        weight = U.get_attr(self.model, key)

        patches = self.patches[key]
        if is_quantized(weight):
            out_weight = weight.to(device_to)
            patches = move_patch_to_device(patches, self.load_device if self.patch_on_device else self.offload_device)
            # TODO: do we ever have legitimate duplicate patches? (i.e. patch on top of patched weight)
            out_weight.patches = [(patches, key)]
        else:
            inplace_update = self.weight_inplace_update or inplace_update
            if key not in self.backup:
                self.backup[key] = WeightBackup(
                    weight.to(device=self.offload_device, copy=inplace_update), inplace_update
                )

            if device_to is not None:
                temp_weight = MM.cast_to_device(weight, device_to, torch.float32, copy=True)
            else:
                temp_weight = weight.to(torch.float32, copy=True)

            out_weight = L.calculate_weight(patches, temp_weight, key)
            out_weight = FL.stochastic_rounding(out_weight, weight.dtype)

        if inplace_update:
            U.copy_to_param(self.model, key, out_weight)
        else:
            U.set_attr_param(self.model, key, out_weight)

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


def update_folder_names_and_paths(key, targets=[]):
    base = FP.folder_names_and_paths.get(key, ([], {}))
    base = base[0] if isinstance(base[0], (list, set, tuple)) else []

    target = next((x for x in targets if x in FP.folder_names_and_paths), targets[0])
    orig, _ = FP.folder_names_and_paths.get(target, ([], {}))
    FP.folder_names_and_paths[key] = (orig or base, {".gguf"})
    if base and base != orig:
        LOG.warning(f"Unknown file list already present on key {key}: {base}")


def _get_dtype(dtype):
    match dtype:
        case None | "default":
            return None
        case "target":
            return dtype
        case _:
            return getattr(torch, dtype)


def load_unet(unet_name, dequant_dtype=None, patch_dtype=None, patch_on_device=None):
    ops = GGMLOps()

    ops.Linear.dequant_dtype = _get_dtype(dequant_dtype)
    ops.Linear.patch_dtype = _get_dtype(patch_dtype)

    unet_path = FP.get_full_path("unet", unet_name)
    sd, extra = gguf_sd_loader(unet_path)

    kwargs = {}
    valid_params = I.signature(SD.load_diffusion_model_state_dict).parameters
    if "metadata" in valid_params:
        kwargs["metadata"] = extra.get("metadata", {})

    model = SD.load_diffusion_model_state_dict(
        sd, model_options={"custom_operations": ops}, **kwargs,
    )

    if model is None:
        raise RuntimeError("ERROR: Could not detect model type of: {}".format(unet_path))

    model = GGUFModelPatcher.clone(model)
    model.patch_on_device = patch_on_device

    return model


def get_filename_list():
    files = []
    files += FP.get_filename_list("clip")
    files += FP.get_filename_list("clip_gguf")
    return sorted(files)


def _load_data(ckpt_paths):
    clip_data = []
    for p in ckpt_paths:
        if p.endswith(".gguf"):
            sd = gguf_clip_loader(p)
        else:
            sd = U.load_torch_file(p, safe_load=True)
            # NOTE: Scaled FP8 would require different custom ops, but only one can be active
            if "scaled_fp8" in sd:
                raise NotImplementedError(
                    f"Mixing scaled FP8 with GGUF is not supported! Use regular CLIP loader or switch model(s)\n({p})")
        clip_data.append(sd)

    return clip_data


def _load_patcher(clip_type, clip_data):
    clip = SD.load_text_encoder_state_dicts(
        clip_type=clip_type,
        state_dicts=clip_data,
        model_options={
            "custom_operations": GGMLOps,
            "initial_device": MM.text_encoder_offload_device()
        },
        embedding_directory=FP.get_folder_paths("embeddings"),
    )
    clip.patcher = GGUFModelPatcher.clone(clip.patcher)

    return clip


def load_clip(clip_name, type="flux2"):
    clip_path = FP.get_full_path("clip", clip_name)
    clip_type = getattr(SD.CLIPType, type.upper(), SD.CLIPType.FLUX2)

    return _load_patcher(clip_type, _load_data([clip_path]))
