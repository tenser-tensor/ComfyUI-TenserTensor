# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import folder_paths as FP

from nodes import VAELoader as VL
from .gguf_loader_helpers import update_folder_names_and_paths, load_unet, get_filename_list, load_clip
from .loader_helpers import load_vae

update_folder_names_and_paths("unet_gguf", ["diffusion_models", "unet"])
update_folder_names_and_paths("clip_gguf", ["text_encoders", "clip"])


class TT_GgufModelsLoader():
    @classmethod
    def INPUT_TYPES(cls):
        unet_names = [x for x in FP.get_filename_list("unet_gguf")]
        clip_names = [x for x in FP.get_filename_list("clip_gguf")]
        vae_names = [x for x in VL.vae_list(VL)]

        return {
            "required": {
                "unet_name": (unet_names,),
                "clip_name": (clip_names,),
                "vae_name": (vae_names,)
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("MODEL", "CLIP", "VAE",)
    FUNCTION = "load_models"
    CATEGORY = "TenserTensor/Loaders/GGUF"

    VAE_DEVICE = "cpu"
    VAE_DTYPE = "bfloat16"

    def load_models(self, unet_name, clip_name, vae_name):
        model = load_unet(unet_name)
        clip = load_clip(clip_name)
        vae = load_vae(vae_name, self.VAE_DEVICE, self.VAE_DTYPE)

        return (model, clip, vae,)
