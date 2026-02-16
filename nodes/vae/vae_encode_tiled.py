class TT_VaeEncodeTiled:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae": ("VAE",),
                "image": ("IMAGE",),
                "tile_width": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                "tile_height": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 32}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)
    FUNCTION = "vae_encode"
    CATEGORY = "TenserTensor/VAE"

    def vae_encode(self, image, vae, tile_width, tile_height, overlap):
        samples = vae.encode_tiled(
            image,
            tile_x=tile_width,
            tile_y=tile_height,
            overlap=overlap
        )
        latent_dict = {"samples": samples}

        return (latent_dict,)
