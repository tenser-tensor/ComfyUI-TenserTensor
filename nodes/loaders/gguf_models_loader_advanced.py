# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import folder_paths as FP

from nodes import VAELoader as VL, MAX_RESOLUTION
from .gguf_loader_helpers import update_folder_names_and_paths, load_unet, load_clip
from .loader_helpers import load_vae, patch_flux_sampling, apply_lora

update_folder_names_and_paths("unet_gguf", ["diffusion_models", "unet"])
update_folder_names_and_paths("clip_gguf", ["text_encoders", "clip"])


class TT_GgufModelsLoaderAdvanced():
    def __init__(self):
        self.loaded_lora_1 = None
        self.loaded_lora_2 = None
        self.loaded_lora_3 = None
        self.loaded_lora_4 = None

    @classmethod
    def INPUT_TYPES(cls):
        UNET_NAMES = [x for x in FP.get_filename_list("unet_gguf")]
        CLIP_NAMES = [x for x in FP.get_filename_list("clip_gguf")]
        LORAS = [x for x in FP.get_filename_list("loras")]
        VAE_NAMES = [x for x in VL.vae_list(VL)]
        DTYPES = ["default", "target", "float32", "float16", "bfloat16"]
        DEVICES = ["default", "cpu"]
        VAE_DTYPES = ["bfloat16", "float16", "float32"]

        return {
            "required": {
                "unet_name": (UNET_NAMES,),
                "dequant_dtype": (DTYPES, {"default": "default", "advanced": True},),
                "patch_dtype": (DTYPES, {"default": "default", "advanced": True},),
                "apply_sampling": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"},),
                "base_sampling_shift": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 100.0, "step": 0.01, "advanced": True},),
                "max_sampling_shift": ("FLOAT", {"default": 1.15, "min": 0.0, "max": 100.0, "step": 0.01, "advanced": True},),
                "sampling_width": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8, "advanced": True},),
                "sampling_height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8, "advanced": True},),
                "lora_name_1": (["None"] + LORAS, {"advanced": True},),
                "strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1, "advanced": True},),
                "lora_name_2": (["None"] + LORAS, {"advanced": True},),
                "strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1, "advanced": True},),
                "lora_name_3": (["None"] + LORAS, {"advanced": True},),
                "strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1, "advanced": True},),
                "lora_name_4": (["None"] + LORAS, {"advanced": True},),
                "strength_4": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1, "advanced": True},),
                "clip_name": (CLIP_NAMES,),
                "vae_name": (VAE_NAMES,),
                "vae_device": (DEVICES, {"advanced": True},),
                "vae_dtype": (VAE_DTYPES, {"advanced": True},),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("MODEL", "CLIP", "VAE",)
    FUNCTION = "load_models"
    CATEGORY = "TenserTensor/Loaders/GGUF"

    def load_models(self, **kwargs):
        model = load_unet(
            kwargs.get("unet_name"),
            kwargs.get("dequant_dtype"),
            kwargs.get("patch_dtype"),
            kwargs.get("patch_on_device")
        )

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

        clip = load_clip(kwargs.get("clip_name"))

        loras = [
            (kwargs.get("lora_name_1"), kwargs.get("strength_1"), 'loaded_lora_1'),
            (kwargs.get("lora_name_2"), kwargs.get("strength_2"), 'loaded_lora_2'),
            (kwargs.get("lora_name_3"), kwargs.get("strength_3"), 'loaded_lora_3'),
            (kwargs.get("lora_name_4"), kwargs.get("strength_4"), 'loaded_lora_4'),
        ]

        for name, strength, attr in loras:
            if name != "None" and strength != 0:
                cached = getattr(self, attr)
                model, clip, lora = apply_lora(cached, model, clip, name, strength)
                setattr(self, attr, lora)

        vae = load_vae(kwargs.get("vae_name"), kwargs.get("vae_device"), kwargs.get("vae_dtype"))

        return (model, clip, vae,)
