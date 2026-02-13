import torch

ASPECT_RATIOS = [
    "1:1",
    "4:3",
    "3:2",
    "16:9",
    "21:9"
]

MEGAPIXELS = [
    "0.25 MP",
    "0.5 MP",
    "1 MP",
    "2 MP",
    "4 MP",
    "8 MP"
]

ORIENTATIONS = [
    "landscape",
    "portrait"
]

MODEL_TYPES = [
    "FLUX",
    "SDXL"
]

CLIP_MULTIPLIERS = [
    "1x",
    "2x",
    "4x"
]


class TT_LatentFactory:
    RETURN_TYPES = ("LATENT", "INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("LATENT", "SEED", "WIDTH", "HEIGHT", "TARGET_WIDTH", "TARGET_HEIGHT")
    FUNCTION = "create_latent"
    CATEGORY = "TenserTensor/Latent"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "aspect_ratio": (ASPECT_RATIOS,),
                "megapixels": (MEGAPIXELS,),
                "orientation": (ORIENTATIONS,),
                "model_type": (MODEL_TYPES,),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}),
                "clip_multiplier": (CLIP_MULTIPLIERS,)
            }
        }

    def calculate_dimensions(self, total_pixels, ratio_w, ratio_h):
        import math

        height = math.sqrt(total_pixels * ratio_h / ratio_w)
        width = height * ratio_w / ratio_h

        width = int(width)
        height = int(height)

        width = round(width / 64) * 64
        height = round(height / 64) * 64

        return width, height

    def create_latent(self, seed, aspect_ratio, megapixels, orientation, model_type, batch_size, clip_multiplier):
        mp_value = float(megapixels.split()[0])
        total_pixels = int(mp_value * 1_000_000)

        ratio_parts = aspect_ratio.split(':')
        ratio_w = int(ratio_parts[0])
        ratio_h = int(ratio_parts[1])

        if orientation == "portrait":
            ratio_w, ratio_h = ratio_h, ratio_w

        width, height = self.calculate_dimensions(total_pixels, ratio_w, ratio_h)

        multiplier = int(clip_multiplier.replace('x', ''))
        clip_width = width * multiplier
        clip_height = height * multiplier

        if model_type == "FLUX":
            channels = 16
        else:
            channels = 4

        latent_width = width // 8
        latent_height = height // 8

        generator = torch.Generator().manual_seed(seed)
        latent = torch.randn(
            batch_size,
            channels,
            latent_height,
            latent_width,
            generator=generator
        )

        latent_dict = {"samples": latent}

        return (latent_dict, seed, width, height, clip_width, clip_height)
