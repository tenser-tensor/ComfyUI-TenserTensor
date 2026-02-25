# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)


from .vae_helpers import vae_decode


class TT_VaeDecodeTiled:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae": ("VAE",),
                "latent": ("LATENT",),
                "tile_width": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                "tile_height": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 32}),
                "circular": ("BOOLEAN", {"default": False, "label_on": "Enabled", "label_off": "Disabled"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "vae_decode"
    CATEGORY = "TenserTensor/VAE"

    def vae_decode(self, latent, vae, tile_width, tile_height, overlap, circular):
        return (vae_decode(latent, vae, tile_width, tile_height, overlap, circular),)
