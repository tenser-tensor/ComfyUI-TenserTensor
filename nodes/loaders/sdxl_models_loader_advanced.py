import folder_paths

from nodes import VAELoader
from .loader_helpers import load_checkpoint, load_sdxl_clip, apply_lora, load_vae


class TT_SdxlModelsLoaderAdvanced:
    def __init__(self):
        self.loaded_lora_1 = None
        self.loaded_lora_2 = None
        self.loaded_lora_3 = None
        self.loaded_lora_4 = None

    @classmethod
    def INPUT_TYPES(cls):
        DEVICES = ["default", "cpu"]
        DTYPES = ["bfloat16", "float16", "float32"]

        return {
            "required": {
                "primary_ckpt": (folder_paths.get_filename_list("checkpoints"),),
                "secondary_ckpt": (["None"] + folder_paths.get_filename_list("checkpoints"),),
                "primary_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "clip_l": (folder_paths.get_filename_list("text_encoders"),),
                "clip_g": (folder_paths.get_filename_list("text_encoders"),),
                "clip_device": (DEVICES, {"advanced": True}),
                "lora_name_1": (["None"] + folder_paths.get_filename_list("loras"),),
                "strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "lora_name_2": (["None"] + folder_paths.get_filename_list("loras"),),
                "strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "lora_name_3": (["None"] + folder_paths.get_filename_list("loras"),),
                "strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "lora_name_4": (["None"] + folder_paths.get_filename_list("loras"),),
                "strength_4": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "vae_name": (VAELoader.vae_list(VAELoader),),
                "vae_device": (DEVICES, {"advanced": True}),
                "vae_dtype": (DTYPES, {"advanced": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("MODEL", "CLIP", "VAE",)
    FUNCTION = "load_models"
    CATEGORY = "TenserTensor/Loaders/SDXL"

    def load_models(self, primary_ckpt, secondary_ckpt, primary_weight, clip_l, clip_g, clip_device,
                    lora_name_1, strength_1, lora_name_2, strength_2, lora_name_3, strength_3, lora_name_4, strength_4,
                    vae_name, vae_device, vae_dtype):

        model = load_checkpoint(primary_ckpt)[0]

        if secondary_ckpt != "None":
            secondary_model = load_checkpoint(secondary_ckpt)[0]
            model = model.clone()
            key_patches = secondary_model.get_key_patches("diffusion_model.")
            for key in key_patches:
                model.add_patches({key: key_patches[key]}, 1.0 - primary_weight, primary_weight)

        clip = load_sdxl_clip(clip_l, clip_g, clip_device)

        loras = [
            (lora_name_1, strength_1, 'loaded_lora_1'),
            (lora_name_2, strength_2, 'loaded_lora_2'),
            (lora_name_3, strength_3, 'loaded_lora_3'),
            (lora_name_4, strength_4, 'loaded_lora_4'),
        ]

        for name, strength, attr in loras:
            if name != "None" and strength != 0:
                cached = getattr(self, attr)
                model, clip, lora = apply_lora(cached, model, clip, name, strength)
                setattr(self, attr, lora)

        vae = load_vae(vae_name, vae_device, vae_dtype)

        return (model, clip, vae,)
