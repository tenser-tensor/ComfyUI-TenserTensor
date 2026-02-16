import folder_paths

from nodes import VAELoader
from .loader_helpers import load_checkpoint, load_sdxl_clip, load_vae


class TT_SdxlModelsLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "primary_ckpt": (folder_paths.get_filename_list("checkpoints"),),
                "secondary_ckpt": (["None"] + folder_paths.get_filename_list("checkpoints"),),
                "primary_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "clip_l": (folder_paths.get_filename_list("text_encoders"),),
                "clip_g": (folder_paths.get_filename_list("text_encoders"),),
                "clip_device": (["default", "cpu"], {"advanced": True}),
                "vae_name": (VAELoader.vae_list(VAELoader),)
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("MODEL", "CLIP", "VAE",)
    FUNCTION = "load_models"
    CATEGORY = "TenserTensor/Loaders/SDXL"

    def load_models(self, primary_ckpt, secondary_ckpt, primary_weight, clip_l, clip_g, clip_device, vae_name):
        model = load_checkpoint(primary_ckpt)[0]

        if secondary_ckpt != "None":
            secondary_model = load_checkpoint(secondary_ckpt)[0]
            model = model.clone()
            key_patches = secondary_model.get_key_patches("diffusion_model.")
            for key in key_patches:
                model.add_patches({key: key_patches[key]}, 1.0 - primary_weight, primary_weight)

        clip = load_sdxl_clip(clip_l, clip_g, clip_device)

        vae = load_vae(vae_name, "cpu", "bfloat16")

        return (model, clip, vae,)
