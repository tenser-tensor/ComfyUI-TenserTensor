# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)
from .vae_helpers import vae_decode


class TT_VaeDecodeContext:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context": ("TT_CONTEXT",),
            }
        }

    RETURN_TYPES = ("TT_CONTEXT", "IMAGE",)
    RETURN_NAMES = ("CONTEXT", "IMAGE",)
    FUNCTION = "vae_decode"
    CATEGORY = "TenserTensor/VAE"

    def vae_decode(self, context):
        vae = context["vae"]
        latent = context["latent"]

        if vae is None:
            raise ValueError("ERROR: VAE is required for decode")
        if latent is None:
            raise ValueError("ERROR: Latent image is required for decode")

        images = vae_decode(latent, vae)
        context["image"] = images

        return (context, images,)
