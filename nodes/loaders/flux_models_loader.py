from folder_paths import get_filename_list

from nodes import VAELoader
from .loader_helpers import load_unet, load_flux_clip, load_vae


class TT_FluxModelsLoader():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "unet_name": (get_filename_list("diffusion_models"),),
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
            unet_name,
            clip_l,
            t5xxl,
            clip_device,
            vae_name
    ):
        model = load_unet(unet_name)
        clip = load_flux_clip(clip_l, t5xxl, clip_device)
        vae = load_vae(vae_name, "cpu", "bfloat16")

        return (model, clip, vae,)
