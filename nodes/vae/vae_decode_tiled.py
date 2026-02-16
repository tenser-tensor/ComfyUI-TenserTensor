import torch


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
        samples = latent["samples"]
        if samples.is_nested:
            samples = samples.unbind()[0]

        if circular == True:
            for layer in [layer for layer in vae.first_stage_model.modules() if isinstance(layer, torch.nn.Conv2d)]:
                layer.padding_mode = "circular"

        compression = vae.spacial_compression_decode()
        images = vae.decode_tiled(
            samples,
            tile_x=tile_width // compression,
            tile_y=tile_height // compression,
            overlap=overlap // compression
        )

        if len(images.shape) == 5:
            images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])

        return (images,)
