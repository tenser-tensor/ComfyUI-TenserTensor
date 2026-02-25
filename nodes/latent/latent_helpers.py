# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.sample as S
import torch
import math


class RandomNoise:
    def __init__(self, seed):
        self.seed = seed

    def generate_noise(self, input_latent):
        latent_image = input_latent["samples"]
        batch_idx = input_latent["batch_index"] if "batch_index" in input_latent else None
        return S.prepare_noise(latent_image, self.seed, batch_idx)


LATENT_DIMENSION_STEP = 64


def _calculate_dimensions(total_pixels, ratio_w, ratio_h):
    height = math.sqrt(total_pixels * ratio_h / ratio_w)
    width = height * ratio_w / ratio_h
    width = int(width)
    height = int(height)
    width = round(width / LATENT_DIMENSION_STEP) * LATENT_DIMENSION_STEP
    height = round(height / LATENT_DIMENSION_STEP) * LATENT_DIMENSION_STEP

    return width, height


def create_empty_latent(seed, noise_seed, aspect_ratio, megapixels, orientation, model_type, batch_size, clip_multiplier):
    mp_value = float(megapixels.split()[0])
    total_pixels = int(mp_value * 1_000_000)

    ratio_parts = aspect_ratio.split(':')
    ratio_w = int(ratio_parts[0])
    ratio_h = int(ratio_parts[1])

    if orientation == "portrait":
        ratio_w, ratio_h = ratio_h, ratio_w

    width, height = _calculate_dimensions(total_pixels, ratio_w, ratio_h)

    multiplier = int(clip_multiplier.replace('x', ''))
    clip_width = width * multiplier
    clip_height = height * multiplier

    match model_type:
        case "FLUX1.D":
            scale_factor = 8
            channels = 16
        case "FLUX2.D":
            scale_factor = 16
            channels = 128
        case "SDXL":
            scale_factor = 8
            channels = 4

    latent_width = width // scale_factor
    latent_height = height // scale_factor

    generator = torch.Generator().manual_seed(seed)
    latent = torch.randn(
        batch_size,
        channels,
        latent_height,
        latent_width,
        generator=generator
    )

    latent_dict = {"samples": latent}
    noise = RandomNoise(noise_seed)

    return (latent_dict, noise, seed, noise_seed, megapixels, width, height, clip_width, clip_height,)


def vae_encode(latent, image, vae):
    tile_width, tile_height, overlap = 512, 512, 64

    samples = vae.encode_tiled(
        image,
        tile_x=tile_width,
        tile_y=tile_height,
        overlap=overlap
    )

    latent["samples"] = samples

    return (latent,)
