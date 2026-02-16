from folder_paths import get_filename_list

from nodes import VAELoader, MAX_RESOLUTION
from .loader_helpers import load_checkpoint, patch_flux_sampling, load_flux_clip, apply_lora, load_vae


class TT_FluxModelsLoaderAdvanced():
    @classmethod
    def INPUT_TYPES(cls):
        DEVICES = ["default", "cpu"]
        DTYPES = ["bfloat16", "float16", "float32"]

        return {
            "required": {
                "ckpt_name": (get_filename_list("checkpoints"),),
                "apply_sampling": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "base_sampling_shift": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 100.0, "step": 0.01}),
                "max_sampling_shift": ("FLOAT", {"default": 1.15, "min": 0.0, "max": 100.0, "step": 0.01}),
                "sampling_width": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                "sampling_height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                "clip_l": (get_filename_list("text_encoders"),),
                "t5xxl": (get_filename_list("text_encoders"),),
                "clip_device": (["default", "cpu"], {"advanced": True}),
                "lora_name_1": (["None"] + get_filename_list("loras"),),
                "strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "lora_name_2": (["None"] + get_filename_list("loras"),),
                "strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "lora_name_3": (["None"] + get_filename_list("loras"),),
                "strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "lora_name_4": (["None"] + get_filename_list("loras"),),
                "strength_4": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "vae_name": (VAELoader.vae_list(VAELoader),),
                "vae_device": (DEVICES, {"advanced": True}),
                "vae_dtype": (DTYPES, {"advanced": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("MODEL", "CLIP", "VAE",)
    FUNCTION = "load_models"
    CATEGORY = "TenserTensor/Loaders/FLUX"

    def load_models(self, **kwargs):
        ckpt_name = kwargs.get("ckpt_name")
        apply_sampling = kwargs.get("apply_sampling")
        model = load_checkpoint(ckpt_name)[0]

        if apply_sampling:
            args = {
                "model": model,
                "base_sampling_shift": kwargs.get("base_sampling_shift"),
                "max_sampling_shift": kwargs.get("max_sampling_shift"),
                "sampling_width": kwargs.get("sampling_width"),
                "sampling_height": kwargs.get("sampling_height"),
            }
            model = patch_flux_sampling(**args)

        clip = load_flux_clip(
            clip_l=kwargs.get("clip_l"),
            t5xxl=kwargs.get("t5xxl"),
            device=kwargs.get("clip_device"),
        )

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
