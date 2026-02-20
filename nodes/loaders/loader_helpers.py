# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import os

import folder_paths as FP
from comfy import model_management as MM, model_sampling as MS, sd as SD, utils as U
from torch import bfloat16, float16, float32, float8_e4m3fn, float8_e5m2, device, tensor

from nodes import VAELoader as VL

VIDEO_TAES = ["taehv", "lighttaew2_2", "lighttaew2_1", "lighttaehy1_5"]
IMAGE_TAES = ["taesd", "taesdxl", "taesd3", "taef1"]


def load_checkpoint(ckpt_name):
    ckpt_path = FP.get_full_path_or_raise("checkpoints", ckpt_name)
    return SD.load_checkpoint_guess_config(
        ckpt_path, output_vae=False, output_clip=False,
        embedding_directory=FP.get_folder_paths("embeddings")
    )


def load_unet(unet_name, unet_dtype="default"):
    unet_path = FP.get_full_path_or_raise("diffusion_models", unet_name)

    model_options = {}
    match unet_dtype:
        case "fp8_e4m3fn":
            model_options["dtype"] = float8_e4m3fn
        case "fp8_e4m3fn_fast":
            model_options["dtype"] = float8_e4m3fn
            model_options["fp8_optimizations"] = True
        case "fp8_e5m2":
            model_options["dtype"] = float8_e5m2
        case _:
            pass

    return SD.load_diffusion_model(
        unet_path,
        model_options=model_options
    )


TORCH_DEVICE_CPU = "cpu"


def _load_clip(clip_type, clip_paths, torch_device=TORCH_DEVICE_CPU):
    model_options = {}
    if torch_device == TORCH_DEVICE_CPU:
        model_options["load_device"] = model_options["offload_device"] = device(TORCH_DEVICE_CPU)

    return SD.load_clip(
        ckpt_paths=clip_paths,
        embedding_directory=FP.get_folder_paths("embeddings"),
        clip_type=clip_type,
        model_options=model_options
    )


def load_sdxl_clip(clip_l, clip_g, device):
    clip_type = getattr(SD.CLIPType, "SDXL", SD.CLIPType.STABLE_DIFFUSION)
    clip_l_path = FP.get_full_path_or_raise("text_encoders", clip_l)
    clip_g_path = FP.get_full_path_or_raise("text_encoders", clip_g)
    clip_paths = [clip_l_path, clip_g_path]

    return _load_clip(clip_type, clip_paths, device)


def load_flux_clip(clip_l, t5xxl, device):
    clip_type = SD.CLIPType.FLUX
    clip_l_path = FP.get_full_path_or_raise("text_encoders", clip_l)
    t5xxl_path = FP.get_full_path_or_raise("text_encoders", t5xxl)
    clip_paths = [clip_l_path, t5xxl_path]

    return _load_clip(clip_type, clip_paths, device)


def apply_lora(loaded_lora, model, clip, lora_name, strength):
    if loaded_lora == None:
        lora_path = FP.get_full_path_or_raise("loras", lora_name)
        lora = U.load_torch_file(lora_path, safe_load=True)
    else:
        lora = loaded_lora

    patched_model, patched_clip = SD.load_lora_for_models(model, clip, lora, strength, strength)

    return (patched_model, patched_clip, lora)


def load_vae(vae_name, vae_device="default", vae_dtype):
    dtype = {"bfloat16": bfloat16, "float16": float16, "float32": float32}[vae_dtype]

    torch_device = None
    if vae_device == "default":
        torch_device = MM.get_torch_device()
    elif vae_device == TORCH_DEVICE_CPU:
        torch_device = device(TORCH_DEVICE_CPU)

    metadata = None
    if vae_name == "pixel_space":
        sd = {}
        sd["pixel_space_vae"] = tensor(1.0)

    elif vae_name in IMAGE_TAES:
        sd = VL.load_taesd(vae_name)

    else:
        if os.path.splitext(vae_name)[0] in VIDEO_TAES:
            vae_path = FP.get_full_path_or_raise("vae_approx", vae_name)
        else:
            vae_path = FP.get_full_path_or_raise("vae", vae_name)
        sd, metadata = U.load_torch_file(vae_path, return_metadata=True)

    vae = SD.VAE(sd=sd, device=torch_device, dtype=dtype, metadata=metadata)
    vae.throw_exception_if_invalid()

    return vae


MIN_SAMPLING_RES = 256
MAX_SAMPLING_RES = 4096


class ModelSamplingFluxAdvanced(MS.ModelSamplingFlux, MS.CONST):
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
