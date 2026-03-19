# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import math
from typing import Any

import torch
from comfy import sample, utils
from comfy.latent_formats import SDXL, Flux, Flux2, SD3
from comfy_api.latest import io, ComfyExtension

from .nodes_image import MEGAPIXELS, resize_image, rotate_image, flip_image
from .nodes_vae import vae_decode, vae_encode

CATEGORY = "TenserTensor/Latent"

ASPECT_RATIOS = ["1:1", "4:3", "3:2", "16:9", "21:9"]
CLIP_MULTIPLIERS = ["1x", "2x", "4x"]
MODEL_TYPES = {
    "FLUX1.D": Flux,
    "FLUX2.D": Flux2,
    "SDXL": SDXL,
    "SD3.X": SD3
}
ORIENTATIONS = ["landscape", "portrait"]
ROTATE_ANGLES = ["90°", "180°", "270°"]
SCALE_METHODS = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]
SCALE_FACTORS = ["0.25x", "0.5x", "1x", "2x", "4x", "8x"]


class RandomNoise:
    def __init__(self, seed):
        self.seed = seed

    def generate_noise(self, input_latent):
        latent_image = input_latent["samples"]
        batch_idx = input_latent["batch_index"] if "batch_index" in input_latent else None

        return sample.prepare_noise(latent_image, self.seed, batch_idx)


LATENT_DIMENSION_STEP = 64


def calculate_dimensions(total_pixels: int, ratio_w: int, ratio_h: int) -> tuple[int, int]:
    height = int(math.sqrt(total_pixels * ratio_h / ratio_w))
    width = int(height * ratio_w / ratio_h)
    width = round(width / LATENT_DIMENSION_STEP) * LATENT_DIMENSION_STEP
    height = round(height / LATENT_DIMENSION_STEP) * LATENT_DIMENSION_STEP
    return width, height


def build_latent(seed: int, batch_size: int, channels: int, latent_width: int, latent_height: int) -> torch.Tensor:
    generator = torch.Generator().manual_seed(seed)
    return torch.randn(batch_size, channels, latent_height, latent_width, generator=generator)


def create_empty_latent(**kwargs) -> tuple[dict[str, Any], int, int]:
    total_pixels = int(float(kwargs.get("megapixels").split()[0]) * 1_000_000)
    ratio_parts = kwargs.get("aspect_ratio").split(':')
    ratio_w, ratio_h = (
        (int(ratio_parts[0]), int(ratio_parts[1]))
        if kwargs.get("orientation") == "landscape"
        else (int(ratio_parts[1]), int(ratio_parts[0]))
    )
    width, height = calculate_dimensions(total_pixels, ratio_w, ratio_h)

    downscale_ratio, channels = None, None

    model = kwargs.get("model")
    if model:
        fmt = model.model.latent_format
        downscale_ratio, channels = fmt.spacial_downscale_ratio, fmt.latent_channels
    else:
        model_type = kwargs.get("model_type")
        fmt = MODEL_TYPES[model_type]()
        downscale_ratio, channels = fmt.spacial_downscale_ratio, fmt.latent_channels

    latent_width, latent_height = width // downscale_ratio, height // downscale_ratio
    latent = build_latent(kwargs.get("seed"), kwargs.get("batch_size"), channels, latent_width, latent_height)

    return {"samples": latent}, width, height


def build(**kwargs):
    samples, width, height = create_empty_latent(**kwargs)
    seed, noise_seed = kwargs.get("seed"), kwargs.get("noise_seed")
    noise = RandomNoise(noise_seed)
    multiplier = int(kwargs.get("clip_multiplier").replace('x', ''))
    clip_width, clip_height = (width * multiplier, height * multiplier,)

    return {
        "latent": samples,
        "noise": noise,
        "seed": seed,
        "noise_seed": noise_seed,
        "megapixels": kwargs.get("megapixels"),
        "width": width,
        "height": height,
        "target_width": clip_width,
        "target_height": clip_height,
    }


class TT_LatentFactoryNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        model_types = list(MODEL_TYPES.keys())

        return io.Schema(
            node_id="TT_LatentFactoryNode",
            display_name="TT Latent Factory",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("noise_seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Combo.Input("aspect_ratio", options=ASPECT_RATIOS),
                io.Combo.Input("megapixels", options=MEGAPIXELS),
                io.Combo.Input("orientation", options=ORIENTATIONS),
                io.Combo.Input("model_type", options=model_types),
                io.Int.Input("batch_size", default=1, min=1, max=64, advanced=True),
                io.Combo.Input("clip_multiplier", options=CLIP_MULTIPLIERS, advanced=True),
            ],
            outputs=[
                io.Latent.Output(display_name="LATENT"),
                io.Noise.Output(display_name="RND_NOISE"),
                io.Int.Output(display_name="SEED"),
                io.Int.Output(display_name="NOISE_SEED"),
                io.String.Output(display_name="MEGAPIXELS"),
                io.Int.Output(display_name="WIDTH"),
                io.Int.Output(display_name="HEIGHT"),
                io.Int.Output(display_name="TARGET_WIDTH"),
                io.Int.Output(display_name="TARGET_HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        args = build(**kwargs)

        return io.NodeOutput(*args.values())


class TT_LatentFactoryByModelNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LatentFactoryByModelNode",
            display_name="TT Latent Factory (By Model)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("noise_seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Combo.Input("aspect_ratio", options=ASPECT_RATIOS),
                io.Combo.Input("megapixels", options=MEGAPIXELS),
                io.Combo.Input("orientation", options=ORIENTATIONS),
                io.Int.Input("batch_size", default=1, min=1, max=64, advanced=True),
                io.Combo.Input("clip_multiplier", options=CLIP_MULTIPLIERS, advanced=True),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Latent.Output(display_name="LATENT"),
                io.Noise.Output(display_name="RND_NOISE"),
                io.Int.Output(display_name="SEED"),
                io.Int.Output(display_name="NOISE_SEED"),
                io.String.Output(display_name="MEGAPIXELS"),
                io.Int.Output(display_name="WIDTH"),
                io.Int.Output(display_name="HEIGHT"),
                io.Int.Output(display_name="TARGET_WIDTH"),
                io.Int.Output(display_name="TARGET_HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        args = build(**kwargs)
        args = {"model": kwargs.get("model"), **args}

        return io.NodeOutput(*args.values())


def set_latent_mask(latent, mask):
    samples = latent
    samples["noise_mask"] = mask.unsqueeze(0) if mask.ndim == 2 else mask

    return samples


def scale_latent(**kwargs):
    samples = kwargs.get("latent")["samples"]
    orig_height, orig_width = samples.shape[2:]
    scale_factor = float(kwargs.get("scale_factor").replace("x", ""))
    final_width, final_height = round(orig_width * scale_factor), round(orig_height * scale_factor)
    scaled = utils.common_upscale(
        samples,
        final_width,
        final_height, kwargs.get("scale_method"),
        "disabled"
    )

    return {"samples": scaled}


def rotate_latent(latent, turns):
    samples = latent["samples"]

    return {"samples": torch.rot90(samples, k=turns, dims=[3, 2])}


def flip_latent(latent, axis):
    samples = latent["samples"]

    return {"samples": torch.flip(samples, dims=[2 if axis == "x" else 3])}


class TT_LatentMultiTransformNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LatentMultiTransformNode",
            display_name="TT Latent MultiTransform",
            category=CATEGORY,
            description="",
            inputs=[
                io.Latent.Input("latent"),
                io.Mask.Input("mask", optional=True),
                io.Boolean.Input("scale_latent", default=True, label_on="Scale", label_off="Skip"),
                io.Combo.Input("scale_factor", options=SCALE_FACTORS, default="1x"),
                io.Combo.Input("scale_method", options=SCALE_METHODS, default="nearest-exact"),
                io.Boolean.Input("rotate_latent", default=True, label_on="Rotate", label_off="Skip"),
                io.Combo.Input("rotate_angle", options=ROTATE_ANGLES),
                io.Boolean.Input("flip_latent", default=True, label_on="Flip", label_off="Skip"),
                io.Combo.Input("flip_direction", options=["horizontal", "vertical"]),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        latent = kwargs.get("latent").copy()

        mask = kwargs.get("mask")
        if mask is not None:
            latent = set_latent_mask(latent, mask)

        if kwargs.get("scale_latent"):
            latent = scale_latent(**kwargs)

        if kwargs.get("rotate_latent"):
            turns = int(kwargs.get("rotate_angle").replace("°", "")) // 90
            latent = rotate_latent(latent, turns)

        if kwargs.get("flip_latent"):
            axis = "x" if kwargs.get("flip_direction") == "vertical" else "y"
            latent = flip_latent(latent, axis)

        return io.NodeOutput(latent)


class TT_LatentMultiTransformOnPixelSpaceNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LatentMultiTransformOnPixelSpaceNode",
            display_name="TT Latent MultiTransform (On Pixel Space)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Vae.Input("vae"),
                io.Latent.Input("latent"),
                io.Mask.Input("mask", optional=True),
                io.Boolean.Input("scale_latent", default=True, label_on="Scale", label_off="Skip"),
                io.Combo.Input("scale_factor", options=SCALE_FACTORS, default="1x"),
                io.Combo.Input("scale_method", options=SCALE_METHODS, default="nearest-exact"),
                io.Boolean.Input("rotate_latent", default=True, label_on="Rotate", label_off="Skip"),
                io.Combo.Input("rotate_angle", options=ROTATE_ANGLES),
                io.Boolean.Input("flip_latent", default=True, label_on="Flip", label_off="Skip"),
                io.Combo.Input("flip_direction", options=["horizontal", "vertical"]),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        latent = kwargs.get("latent").copy()
        vae = kwargs.get("vae")
        pixels = vae_decode(latent, vae)
        orig_height, orig_width = pixels.shape[1:3]

        if kwargs.get("scale_latent"):
            scale_factor = float(kwargs.get("scale_factor").replace("x", ""))
            pixels = resize_image(
                pixels,
                int(orig_width * scale_factor),
                int(orig_height * scale_factor),
                kwargs.get("scale_method"),
            )

        if kwargs.get("rotate_latent"):
            turns = int(kwargs.get("rotate_angle").replace("°", "")) // 90
            pixels = rotate_image(pixels, turns)

        if kwargs.get("flip_latent"):
            axis = "x" if kwargs.get("flip_direction") == "vertical" else "y"
            pixels = flip_image(pixels, axis)

        latent = vae_encode(pixels, vae)

        mask = kwargs.get("mask")
        if mask is not None:
            latent = set_latent_mask(latent, mask)

        return io.NodeOutput(latent)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

NODES = [
    TT_LatentFactoryNode,
    TT_LatentFactoryByModelNode,
    TT_LatentMultiTransformNode,
    TT_LatentMultiTransformOnPixelSpaceNode,
]
