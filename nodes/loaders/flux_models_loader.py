from folder_paths import get_filename_list

from nodes import VAELoader
from .loader_helpers import load_checkpoint, load_flux_clip, load_vae


class TT_FluxModelsLoader():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ckpt_name": (get_filename_list("checkpoints"),),
                "clip_l": (get_filename_list("text_encoders"),),
                "t5xxl": (get_filename_list("text_encoders"),),
                "clip_device": (["default", "cpu"], {"advanced": True}),
                "vae_name": (VAELoader.vae_list(VAELoader),)
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("MODEL", "CLIP", "VAE",)
    FUNCTION = "load_models"
    CATEGORY = "TenserTensor/Loaders/FLUX"

    def load_models(
            self,
            ckpt_name,
            clip_l,
            t5xxl,
            clip_device,
            vae_name
    ):
        model = load_checkpoint(ckpt_name)[0]
        clip = load_flux_clip(clip_l, t5xxl, clip_device)
        vae = load_vae(vae_name, "cpu", "bfloat16")

        return (model, clip, vae,)
