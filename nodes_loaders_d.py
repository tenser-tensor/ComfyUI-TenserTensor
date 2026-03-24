# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

# Contains slightly modified code by City96
# (c) City96 || Apache-2.0 (apache.org/licenses/LICENSE-2.0)
# Modified by TenserTensor
# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import collections
import inspect
import os

import folder_paths
import torch
from comfy import sd, model_management, utils, model_sampling, model_patcher, lora, float
from comfy_api.latest import io, ComfyExtension
from torch import bfloat16, float16, float32, float8_e4m3fn, float8_e5m2, device, tensor

from nodes import VAELoader, MAX_RESOLUTION
from .gguf.dequant import is_quantized, is_torch_compatible
from .gguf.loader import gguf_sd_loader, gguf_clip_loader
from .gguf.ops import GGMLOps, move_patch_to_device

CATEGORY = "TenserTensor/Loaders"
D_CATEGORY = "TenserTensor/Deprecated/Loaders"
TORCH_DEVICES = ["default", "cpu"]
TORCH_DEVICE_CPU = "cpu"
DTYPES = {"bfloat16": bfloat16, "float16": float16, "float32": float32}
VIDEO_TAES = ["taehv", "lighttaew2_2", "lighttaew2_1", "lighttaehy1_5"]
IMAGE_TAES = ["taesd", "taesdxl", "taesd3", "taef1"]
MIN_SAMPLING_RES = 256
MAX_SAMPLING_RES = 4096


def get_checkpoint_files():
    return folder_paths.get_filename_list("checkpoints")


def get_diffusion_models_files():
    return folder_paths.get_filename_list("diffusion_models")


def get_gguf_diffusion_models_files():
    update_folder_names_and_paths("diffusion_models_gguf", "diffusion_models", {".gguf"})

    return [f for f in folder_paths.get_filename_list("diffusion_models_gguf")]


def get_text_encoder_files():
    return folder_paths.get_filename_list("text_encoders")


def get_gguf_text_encoder_files():
    update_folder_names_and_paths("text_encoders_gguf", "text_encoders", {'.gguf', '.pt', '.pth', '.safetensors'})

    return [x for x in folder_paths.get_filename_list("text_encoders_gguf")]


def get_vae_files():
    return VAELoader.vae_list(VAELoader)


def get_lora_files():
    return ["None"] + folder_paths.get_filename_list("loras")

def get_embedding_directory():
    return folder_paths.get_folder_paths("embeddings")

def load_checkpoint(checkpoint):
    ckpt_path = folder_paths.get_full_path_or_raise("checkpoints", checkpoint)

    return sd.load_checkpoint_guess_config(
        ckpt_path, output_vae=False, output_clip=False,
        embedding_directory=get_embedding_directory()
    )[0]


def load_sdxl_clip(clip_l, clip_g, clip_device):
    clip_type = getattr(sd.CLIPType, "SDXL", sd.CLIPType.STABLE_DIFFUSION)
    clip_l_path = folder_paths.get_full_path_or_raise("text_encoders", clip_l)
    clip_g_path = folder_paths.get_full_path_or_raise("text_encoders", clip_g)

    model_options = {}
    if clip_device == TORCH_DEVICE_CPU:
        model_options["load_device"] = model_options["offload_device"] = device(TORCH_DEVICE_CPU)

    return sd.load_clip(
        ckpt_paths=[clip_l_path, clip_g_path],
        embedding_directory=folder_paths.get_folder_paths("embeddings"),
        clip_type=clip_type,
        model_options=model_options
    )


def load_vae(vae_name, vae_device="default", vae_dtype="bfloat16"):
    dtype = DTYPES[vae_dtype]
    torch_device = model_management.get_torch_device() if vae_device == "default" else device(vae_device)

    metadata = None
    if vae_name == "pixel_space":
        state_dict = {"pixel_space_vae": tensor(1.0)}
    elif vae_name in IMAGE_TAES:
        state_dict = VAELoader.load_taesd(vae_name)
    else:
        vae_path = (
            folder_paths.get_full_path_or_raise("vae_approx", vae_name)
            if os.path.splitext(vae_name)[0] in VIDEO_TAES
            else folder_paths.get_full_path_or_raise("vae", vae_name)
        )
        state_dict, metadata = utils.load_torch_file(vae_path, return_metadata=True)

    vae = sd.VAE(sd=state_dict, device=torch_device, dtype=dtype, metadata=metadata)
    vae.throw_exception_if_invalid()

    return vae


def load_sdxl_pipeline(cls, apply_loras, **kwargs):
    model = load_checkpoint(kwargs.get("primary_ckpt"))

    secondary_ckpt = kwargs.get("secondary_ckpt")
    if secondary_ckpt != "None":
        primary_weight = kwargs.get("primary_weight")
        secondary_model = load_checkpoint(secondary_ckpt)
        model = model.clone()
        key_patches = secondary_model.get_key_patches("diffusion_model.")
        for key in key_patches:
            model.add_patches({key: key_patches[key]}, 1.0 - primary_weight, primary_weight)

    clip_l, clip_g, clip_device = (
        kwargs.get("clip_l"),
        kwargs.get("clip_g"),
        kwargs.get("clip_device"),
    )
    clip = load_sdxl_clip(clip_l, clip_g, clip_device)

    if apply_loras:
        loras = [
            (kwargs.get("lora_name_1"), kwargs.get("strength_1"), 'loaded_lora_1'),
            (kwargs.get("lora_name_2"), kwargs.get("strength_2"), 'loaded_lora_2'),
            (kwargs.get("lora_name_3"), kwargs.get("strength_3"), 'loaded_lora_3'),
            (kwargs.get("lora_name_4"), kwargs.get("strength_4"), 'loaded_lora_4'),
        ]

        for name, strength, attr in loras:
            if name != "None" and strength != 0:
                cached = getattr(cls, attr)
                model, clip, lora = apply_lora(cached, model, clip, name, strength)
                setattr(cls, attr, lora)

    vae = load_vae(kwargs.get("vae_name"), kwargs.get("vae_device"), kwargs.get("vae_dtype"))

    return model, clip, vae


class TT_SdxlModelsLoaderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_SdxlModelsLoaderNode",
            display_name="TT SDXL Models Loader",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("primary_ckpt", options=get_checkpoint_files()),
                io.Combo.Input("secondary_ckpt", options=["None"] + get_checkpoint_files()),
                io.Float.Input("primary_weight", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Combo.Input("clip_l", options=get_text_encoder_files()),
                io.Combo.Input("clip_g", options=get_text_encoder_files()),
                io.Combo.Input("clip_device", options=TORCH_DEVICES, default="default"),
                io.Combo.Input("vae_name", options=get_vae_files()),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        model, clip, vae = load_sdxl_pipeline(cls, apply_loras=False, **kwargs)

        return io.NodeOutput(model, clip, vae)


def apply_lora(loaded_lora, model, clip, lora_name, strength):
    if loaded_lora is None:
        lora_path = folder_paths.get_full_path_or_raise("loras", lora_name)
        lora = utils.load_torch_file(lora_path, safe_load=True)
    else:
        lora = loaded_lora

    patched_model, patched_clip = sd.load_lora_for_models(model, clip, lora, strength, strength)

    return (patched_model, patched_clip, lora)


class TT_SdxlModelsLoaderAdvancedNode(io.ComfyNode):
    loaded_lora_1 = None
    loaded_lora_2 = None
    loaded_lora_3 = None
    loaded_lora_4 = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_SdxlModelsLoaderAdvancedNode",
            display_name="TT SDXL Models Loader (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("primary_ckpt", options=get_checkpoint_files()),
                io.Combo.Input("secondary_ckpt", options=["None"] + get_checkpoint_files()),
                io.Float.Input("primary_weight", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Combo.Input("clip_l", options=get_text_encoder_files()),
                io.Combo.Input("clip_g", options=get_text_encoder_files()),
                io.Combo.Input("clip_device", options=TORCH_DEVICES, default="default"),
                io.Combo.Input("lora_name_1", options=get_lora_files()),
                io.Float.Input("strength_1", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_2", options=get_lora_files()),
                io.Float.Input("strength_2", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_3", options=get_lora_files()),
                io.Float.Input("strength_3", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_4", options=get_lora_files()),
                io.Float.Input("strength_4", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("vae_name", options=get_vae_files()),
                io.Combo.Input("vae_device", options=TORCH_DEVICES, default="default"),
                io.Combo.Input("vae_dtype", options=list(DTYPES.keys())),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        model, clip, vae = load_sdxl_pipeline(cls, apply_loras=True, **kwargs)

        return io.NodeOutput(model, clip, vae)


def load_diffusion_model(diffusion_model, dtype="default"):
    unet_path = folder_paths.get_full_path_or_raise("diffusion_models", diffusion_model)

    model_options = {}
    match dtype:
        case "fp8_e4m3fn":
            model_options["dtype"] = float8_e4m3fn
        case "fp8_e4m3fn_fast":
            model_options["dtype"] = float8_e4m3fn
            model_options["fp8_optimizations"] = True
        case "fp8_e5m2":
            model_options["dtype"] = float8_e5m2
        case _:
            pass

    return sd.load_diffusion_model(unet_path, model_options=model_options)


def load_flux_clip(clip_l, t5xxl, device):
    clip_type = sd.CLIPType.FLUX
    clip_l_path = folder_paths.get_full_path_or_raise("text_encoders", clip_l)
    t5xxl_path = folder_paths.get_full_path_or_raise("text_encoders", t5xxl)

    model_options = {}
    if device == TORCH_DEVICE_CPU:
        model_options["load_device"] = model_options["offload_device"] = device(TORCH_DEVICE_CPU)

    return sd.load_clip(
        ckpt_paths=[clip_l_path, t5xxl_path],
        embedding_directory=folder_paths.get_folder_paths("embeddings"),
        clip_type=clip_type,
        model_options=model_options
    )


class ModelSamplingFluxAdvanced(model_sampling.ModelSamplingFlux, model_sampling.CONST):
    pass


def patch_flux_sampling(model, base_sampling_shift, max_sampling_shift, sampling_width, sampling_height):
    tmodel = model.clone()

    slope = (max_sampling_shift - base_sampling_shift) / (MAX_SAMPLING_RES - MIN_SAMPLING_RES)
    intercept = base_sampling_shift - slope * MIN_SAMPLING_RES
    current_res = (sampling_width * sampling_height / (8 * 8 * 2 * 2))
    shift = current_res * slope + intercept

    model_sampling = ModelSamplingFluxAdvanced(model.model.model_config)
    model_sampling.set_parameters(shift=shift)
    tmodel.add_object_patch("model_sampling", model_sampling)

    return tmodel


def load_flux_pipeline(cls, apply_loras=False, **kwargs):
    model = load_diffusion_model(kwargs.get("diffusion_model"))

    if kwargs.get("apply_sampling"):
        args = {
            "model": model,
            "base_sampling_shift": kwargs.get("base_sampling_shift"),
            "max_sampling_shift": kwargs.get("max_sampling_shift"),
            "sampling_width": kwargs.get("sampling_width"),
            "sampling_height": kwargs.get("sampling_height"),
        }
        model = patch_flux_sampling(**args)

    clip = load_flux_clip(
        kwargs.get("clip_l"),
        kwargs.get("t5xxl"),
        kwargs.get("clip_device"),
    )

    if apply_loras:
        loras = [
            (kwargs.get("lora_name_1"), kwargs.get("strength_1"), 'loaded_lora_1'),
            (kwargs.get("lora_name_2"), kwargs.get("strength_2"), 'loaded_lora_2'),
            (kwargs.get("lora_name_3"), kwargs.get("strength_3"), 'loaded_lora_3'),
            (kwargs.get("lora_name_4"), kwargs.get("strength_4"), 'loaded_lora_4'),
        ]

        for name, strength, attr in loras:
            if name != "None" and strength != 0:
                cached = getattr(cls, attr)
                model, clip, lora = apply_lora(cached, model, clip, name, strength)
                setattr(cls, attr, lora)

    vae = load_vae(kwargs.get("vae_name"), kwargs.get("vae_device"), kwargs.get("vae_dtype"))

    return (model, clip, vae,)


class TT_FluxModelsLoaderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_FluxModelsLoaderNode",
            display_name="TT FLUX Models Loader",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_diffusion_models_files()),
                io.Combo.Input("clip_l", options=get_text_encoder_files()),
                io.Combo.Input("t5xxl", options=get_text_encoder_files()),
                io.Combo.Input("clip_device", options=TORCH_DEVICES, default="default"),
                io.Combo.Input("vae_name", options=get_vae_files()),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        model, clip, vae = load_flux_pipeline(cls, apply_loras=False, **kwargs)

        return io.NodeOutput(model, clip, vae)


class TT_FluxModelsLoaderAdvancedNode(io.ComfyNode):
    loaded_lora_1 = None
    loaded_lora_2 = None
    loaded_lora_3 = None
    loaded_lora_4 = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_FluxModelsLoaderAdvancedNode",
            display_name="TT FLUX Models Loader (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_diffusion_models_files()),
                io.Boolean.Input("apply_sampling", default=True, label_on="Flux Shift", label_off="No Shift"),
                io.Float.Input("base_sampling_shift", default=0.5, min=0.0, max=100.0, step=0.01, advanced=True),
                io.Float.Input("max_sampling_shift", default=1.15, min=0.0, max=100.0, step=0.01, advanced=True),
                io.Int.Input("sampling_width", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Int.Input("sampling_height", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Combo.Input("clip_l", options=get_text_encoder_files()),
                io.Combo.Input("t5xxl", options=get_text_encoder_files()),
                io.Combo.Input("clip_device", options=TORCH_DEVICES, default="default", advanced=True),
                io.Combo.Input("lora_name_1", options=get_lora_files()),
                io.Float.Input("strength_1", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_2", options=get_lora_files()),
                io.Float.Input("strength_2", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_3", options=get_lora_files()),
                io.Float.Input("strength_3", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_4", options=get_lora_files()),
                io.Float.Input("strength_4", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("vae_name", options=get_vae_files()),
                io.Combo.Input("vae_device", options=TORCH_DEVICES, default="default", advanced=True),
                io.Combo.Input("vae_dtype", options=list(DTYPES.keys()), advanced=True),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        model, clip, vae = load_flux_pipeline(cls, apply_loras=True, **kwargs)

        return io.NodeOutput(model, clip, vae)


def update_folder_names_and_paths(folder, base_folder=None, exts=None):
    if folder in folder_paths.folder_names_and_paths:
        return

    path = os.path.join(folder_paths.models_dir, folder)
    os.makedirs(path, exist_ok=True)
    paths = [path]
    base_paths, base_exts = folder_paths.folder_names_and_paths.get(base_folder, ([], {})) if base_folder else ([], {})
    _exts = exts if exts is not None else base_exts
    folder_paths.folder_names_and_paths[folder] = (paths + base_paths, _exts)


WeightBackup = collections.namedtuple('WeightBackup', ['weight', 'inplace_update'])


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
                self.backup[key] = WeightBackup(
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


def get_dtype(dtype):
    match dtype:
        case None | "default":
            return None
        case "target":
            return dtype
        case _:
            return getattr(torch, dtype)


def load_clip_data(ckpt_paths):
    clip_data = []
    for path in ckpt_paths:
        if path.endswith(".gguf"):
            state_dict = gguf_clip_loader(path)
        else:
            state_dict = utils.load_torch_file(path, safe_load=True)
            # NOTE: Scaled FP8 would require different custom ops, but only one can be active
            if "scaled_fp8" in state_dict:
                raise NotImplementedError(
                    f"Mixing scaled FP8 with GGUF is not supported! Use regular CLIP loader or switch model(s)\n({path})")

        clip_data.append(state_dict)

    return clip_data


def load_flux_clip_patcher(clip_name, type="flux2"):
    clip_path = folder_paths.get_full_path("text_encoders_gguf", clip_name)
    clip_type = getattr(sd.CLIPType, type.upper(), sd.CLIPType.FLUX2)
    clip_data = load_clip_data([clip_path])

    clip = sd.load_text_encoder_state_dicts(
        clip_type=clip_type,
        state_dicts=clip_data,
        model_options={
            "custom_operations": GGMLOps,
            "initial_device": model_management.text_encoder_offload_device()
        },
        embedding_directory=folder_paths.get_folder_paths("embeddings"),
    )
    clip.patcher = GGUFModelPatcher.clone(clip.patcher)

    return clip


def load_sd3_clip_patcher(clip_l, clip_g, t5xxl, type="sd3"):
    clip_l_path = folder_paths.get_full_path("text_encoders_gguf", clip_l)
    clip_g_path = folder_paths.get_full_path("text_encoders_gguf", clip_g)
    t5xxl_path = folder_paths.get_full_path("text_encoders_gguf", t5xxl)
    clip_type = getattr(sd.CLIPType, type.upper(), sd.CLIPType.SD3)
    clip_data = load_clip_data([clip_l_path, clip_g_path, t5xxl_path])

    clip = sd.load_text_encoder_state_dicts(
        clip_type=clip_type,
        state_dicts=clip_data,
        model_options={
            "custom_operations": GGMLOps,
            "initial_device": model_management.text_encoder_offload_device()
        },
        embedding_directory=folder_paths.get_folder_paths("embeddings"),
    )
    clip.patcher = GGUFModelPatcher.clone(clip.patcher)

    return clip


def apply_bypass_lora_for_models(loaded_lora, model, clip, lora_name, strength):
    if loaded_lora == None:
        lora_path = folder_paths.get_full_path_or_raise("loras", lora_name)
        lora = utils.load_torch_file(lora_path, safe_load=True)
    else:
        lora = loaded_lora

    patched_model, patched_clip = sd.load_bypass_lora_for_models(model, clip, lora, strength, strength)

    return (patched_model, patched_clip, lora,)


def load_gguf_pipeline(cls, **kwargs):
    ops = GGMLOps()

    ops.Linear.dequant_dtype = get_dtype(kwargs.get("dequant_dtype", None))
    ops.Linear.patch_dtype = get_dtype(kwargs.get("patch_dtype", None))

    gguf_full_path = folder_paths.get_full_path("diffusion_models_gguf", kwargs.get("diffusion_model"))
    state_dict, extra = gguf_sd_loader(gguf_full_path)

    args = {}
    valid_params = inspect.signature(sd.load_diffusion_model_state_dict).parameters

    if "metadata" in valid_params:
        args["metadata"] = extra.get("metadata", {})

    model = sd.load_diffusion_model_state_dict(state_dict, model_options={"custom_operations": ops}, **args, )

    if model is None:
        raise RuntimeError("ERROR: Could not detect model type of: {}".format(gguf_full_path))

    model = GGUFModelPatcher.clone(model)
    model.patch_on_device = kwargs.get("patch_on_device", None)

    apply_sampling = kwargs.get("apply_sampling")
    if apply_sampling:
        args = {
            "model": model,
            "base_sampling_shift": kwargs.get("base_sampling_shift"),
            "max_sampling_shift": kwargs.get("max_sampling_shift"),
            "sampling_width": kwargs.get("sampling_width"),
            "sampling_height": kwargs.get("sampling_height"),
        }
        model = patch_flux_sampling(**args)

    clip_name = kwargs.get("clip")
    if clip_name:
        clip = load_flux_clip_patcher(kwargs.get("clip"), kwargs.get("clip_type", "flux2"))
    else:
        clip_l, clip_g, t5xxl = kwargs.get("clip_l"), kwargs.get("clip_g"), kwargs.get("t5xxl")
        clip = load_sd3_clip_patcher(clip_l, clip_g, t5xxl)

    if kwargs.get("apply_bypass_lora"):
        loras = [
            (kwargs.get("lora_name_1"), kwargs.get("strength_1"), 'loaded_lora_1'),
            (kwargs.get("lora_name_2"), kwargs.get("strength_2"), 'loaded_lora_2'),
            (kwargs.get("lora_name_3"), kwargs.get("strength_3"), 'loaded_lora_3'),
            (kwargs.get("lora_name_4"), kwargs.get("strength_4"), 'loaded_lora_4'),
        ]

        for name, strength, attr in loras:
            if name != "None" and strength != 0:
                cached = getattr(cls, attr)
                model, clip, lora = apply_bypass_lora_for_models(cached, model, clip, name, strength)
                setattr(cls, attr, lora)

    vae = load_vae(
        kwargs.get("vae_name"),
        kwargs.get("vae_device", "default"),
        kwargs.get("vae_dtype", "bfloat16"),
    )

    return model, clip, vae


class TT_Flux2GgufModelsLoaderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux2GgufModelsLoaderNode",
            display_name="TT FLUX2 GGUF Models Loader",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_gguf_diffusion_models_files()),
                io.Combo.Input("clip", options=get_gguf_text_encoder_files()),
                io.Combo.Input("vae_name", options=get_vae_files()),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["apply_bypass_lora"] = False
        model, clip, vae = load_gguf_pipeline(cls, apply_loras=True, **kwargs)

        return io.NodeOutput(model, clip, vae)


class TT_Flux2GgufModelsLoaderAdvancedNode(io.ComfyNode):
    loaded_lora_1 = None
    loaded_lora_2 = None
    loaded_lora_3 = None
    loaded_lora_4 = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux2GgufModelsLoaderAdvancedNode",
            display_name="TT FLUX2 GGUF Models Loader (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_gguf_diffusion_models_files()),
                io.Combo.Input("dequant_dtype", options=list(DTYPES.keys()), default="bfloat16", advanced=True),
                io.Combo.Input("patch_dtype", options=list(DTYPES.keys()), default="bfloat16", advanced=True),
                io.Boolean.Input("apply_sampling", default=True, label_on="Flux Shift", label_off="No Shift"),
                io.Float.Input("base_sampling_shift", default=0.5, min=0.0, max=100.0, step=0.01, advanced=True),
                io.Float.Input("max_sampling_shift", default=1.15, min=0.0, max=100.0, step=0.01, advanced=True),
                io.Int.Input("sampling_width", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Int.Input("sampling_height", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Combo.Input("clip", options=get_gguf_text_encoder_files()),
                io.Combo.Input("clip_device", options=TORCH_DEVICES, default="default", advanced=True),
                io.Combo.Input("lora_name_1", options=get_lora_files()),
                io.Float.Input("strength_1", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_2", options=get_lora_files()),
                io.Float.Input("strength_2", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_3", options=get_lora_files()),
                io.Float.Input("strength_3", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_4", options=get_lora_files()),
                io.Float.Input("strength_4", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("vae_name", options=get_vae_files()),
                io.Combo.Input("vae_device", options=TORCH_DEVICES, default="default", advanced=True),
                io.Combo.Input("vae_dtype", options=list(DTYPES.keys()), advanced=True),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["apply_bypass_lora"] = False
        model, clip, vae = load_gguf_pipeline(cls, apply_loras=True, **kwargs)

        return io.NodeOutput(model, clip, vae)


class TT_Sd35GgufModelsLoaderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Sd35GgufModelsLoaderNode",
            display_name="TT SD3.5 GGUF Models Loader",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_gguf_diffusion_models_files()),
                io.Combo.Input("clip_l", options=get_gguf_text_encoder_files()),
                io.Combo.Input("clip_g", options=get_gguf_text_encoder_files()),
                io.Combo.Input("t5xxl", options=get_gguf_text_encoder_files()),
                io.Combo.Input("vae_name", options=get_vae_files()),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["apply_bypass_lora"] = False
        model, clip, vae = load_gguf_pipeline(cls, apply_loras=True, **kwargs)

        return io.NodeOutput(model, clip, vae)


class TT_Sd35GgufModelsLoaderAdvancedNode(io.ComfyNode):
    loaded_lora_1 = None
    loaded_lora_2 = None
    loaded_lora_3 = None
    loaded_lora_4 = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Sd35GgufModelsLoaderAdvancedNode",
            display_name="TT SD3.5 GGUF Models Loader (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_gguf_diffusion_models_files()),
                io.Combo.Input("dequant_dtype", options=list(DTYPES.keys()), default="bfloat16", advanced=True),
                io.Combo.Input("patch_dtype", options=list(DTYPES.keys()), default="bfloat16", advanced=True),
                io.Combo.Input("clip_l", options=get_gguf_text_encoder_files()),
                io.Combo.Input("clip_g", options=get_gguf_text_encoder_files()),
                io.Combo.Input("t5xxl", options=get_gguf_text_encoder_files()),
                io.Combo.Input("clip_device", options=TORCH_DEVICES, default="default", advanced=True),
                io.Combo.Input("lora_name_1", options=get_lora_files()),
                io.Float.Input("strength_1", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_2", options=get_lora_files()),
                io.Float.Input("strength_2", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_3", options=get_lora_files()),
                io.Float.Input("strength_3", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("lora_name_4", options=get_lora_files()),
                io.Float.Input("strength_4", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("vae_name", options=get_vae_files()),
                io.Combo.Input("vae_device", options=TORCH_DEVICES, default="default", advanced=True),
                io.Combo.Input("vae_dtype", options=list(DTYPES.keys()), advanced=True),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("CLIP"),
                io.Vae.Output("VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["apply_bypass_lora"] = True
        model, clip, vae = load_gguf_pipeline(cls, apply_loras=True, **kwargs)

        return io.NodeOutput(model, clip, vae)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

NODES = [
    TT_SdxlModelsLoaderNode,
    TT_SdxlModelsLoaderAdvancedNode,
    TT_FluxModelsLoaderNode,
    TT_FluxModelsLoaderAdvancedNode,
    TT_Flux2GgufModelsLoaderNode,
    TT_Flux2GgufModelsLoaderAdvancedNode,
    TT_Sd35GgufModelsLoaderNode,
    TT_Sd35GgufModelsLoaderAdvancedNode,
]
