# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import math
from typing import Any

import torch

from comfy import sample, utils, model_management
from comfy.nested_tensor import NestedTensor
from comfy_api.latest import io
from comfy_api.latest._io import NodeOutput
from .nodes_image import resize_image, rotate_image, flip_image
from .nodes_vae import vae_decode, vae_encode
from .utils import CommonTypes

CATEGORY = "TenserTensor/Latent"


class RandomNoise:
    def __init__(self, seed):
        self.seed = seed

    def generate_noise(self, input_latent):
        latent_image = input_latent["samples"]
        batch_idx = input_latent["batch_index"] if "batch_index" in input_latent else None

        return sample.prepare_noise(latent_image, self.seed, batch_idx)


def calculate_dimensions(total_pixels: int, ratio_w: int, ratio_h: int) -> tuple[int, int]:
    latent_dimension_step = CommonTypes.LATENT_DIMENSION_STEP
    height = int(math.sqrt(total_pixels * ratio_h / ratio_w))
    width = int(height * ratio_w / ratio_h)
    width = round(width / latent_dimension_step) * latent_dimension_step
    height = round(height / latent_dimension_step) * latent_dimension_step

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
    model = kwargs.get("model")
    if model:
        fmt = model.model.latent_format
        downscale_ratio, channels = fmt.spacial_downscale_ratio, fmt.latent_channels
    else:
        model_type = kwargs.get("model_type")
        fmt = CommonTypes.MODEL_TYPES[model_type]()
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
        model_types = list(CommonTypes.MODEL_TYPES.keys())

        return io.Schema(
            node_id="TT_LatentFactoryNode",
            display_name="TT Latent Factory",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("noise_seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Combo.Input("aspect_ratio", options=CommonTypes.ASPECT_RATIOS),
                io.Combo.Input("megapixels", options=CommonTypes.MEGAPIXELS),
                io.Combo.Input("orientation", options=CommonTypes.ORIENTATIONS),
                io.Combo.Input("model_type", options=model_types),
                io.Int.Input("batch_size", default=1, min=1, max=64, advanced=True),
                io.Combo.Input("clip_multiplier", options=CommonTypes.CLIP_MULTIPLIERS, advanced=True),
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
                io.Combo.Input("aspect_ratio", options=CommonTypes.ASPECT_RATIOS),
                io.Combo.Input("megapixels", options=CommonTypes.MEGAPIXELS),
                io.Combo.Input("orientation", options=CommonTypes.ORIENTATIONS),
                io.Int.Input("batch_size", default=1, min=1, max=64, advanced=True),
                io.Combo.Input("clip_multiplier", options=CommonTypes.CLIP_MULTIPLIERS, advanced=True),
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
                io.Combo.Input("scale_factor", options=CommonTypes.SCALE_FACTORS, default="1x"),
                io.Combo.Input("scale_method", options=CommonTypes.SCALE_METHODS, default="nearest-exact"),
                io.Boolean.Input("rotate_latent", default=True, label_on="Rotate", label_off="Skip"),
                io.Combo.Input("rotate_angle", options=CommonTypes.ROTATE_ANGLES),
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
                io.Combo.Input("scale_factor", options=CommonTypes.SCALE_FACTORS, default="1x"),
                io.Combo.Input("scale_method", options=CommonTypes.SCALE_METHODS, default="nearest-exact"),
                io.Boolean.Input("rotate_latent", default=True, label_on="Rotate", label_off="Skip"),
                io.Combo.Input("rotate_angle", options=CommonTypes.ROTATE_ANGLES),
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


def calc_total_length(**kwargs):
    video_vae, length_sec, frame_rate, batch_size = (
        kwargs.get("video_vae"),
        kwargs.get("length_sec"),
        kwargs.get("frame_rate"),
        kwargs.get("batch_size"),
    )
    temporal_compression_ratio = video_vae.temporal_compression_ratio
    fps = int(frame_rate.replace('fps', ''))
    frames_count = length_sec * fps
    total_length = ((frames_count - 1) // temporal_compression_ratio) * temporal_compression_ratio + 1

    return total_length, fps


def create_empty_video_latent(**kwargs):
    total_length, fps = calc_total_length(**kwargs)
    video_vae, megapixels, orientation = kwargs.get("video_vae"), kwargs.get("megapixels"), kwargs.get("orientation")

    total_pixels = int(float(megapixels.split()[0]) * 1_000_000)
    ratio_parts = kwargs.get("aspect_ratio").split(':')
    ratio_w, ratio_h = (
        (int(ratio_parts[0]), int(ratio_parts[1]))
        if orientation == "landscape"
        else (int(ratio_parts[1]), int(ratio_parts[0]))
    )
    width, height = calculate_dimensions(total_pixels, ratio_w, ratio_h)

    generator = torch.Generator().manual_seed(kwargs.get("seed"))
    video_samples = torch.randn(
        kwargs.get("batch_size"),
        video_vae.latent_channels,
        total_length,
        height // video_vae.spacial_downscale_ratio,
        width // video_vae.spacial_downscale_ratio,
        generator=generator,
        device=model_management.intermediate_device()
    )

    return {"samples": video_samples}


def create_empty_audio_latent(**kwargs):
    total_length, fps = calc_total_length(**kwargs)
    audio_vae = kwargs.get("audio_vae")

    channels = audio_vae.latent_channels
    audio_freq = audio_vae.latent_frequency_bins
    sampling_rate = int(audio_vae.sample_rate)
    num_audio_latents = audio_vae.num_of_latents_from_frames(total_length, fps)

    generator = torch.Generator().manual_seed(kwargs.get("seed"))
    audio_samples = torch.randn(
        kwargs.get("batch_size"), channels, num_audio_latents, audio_freq,
        generator=generator, device=model_management.intermediate_device()
    )

    return {
        "samples": audio_samples,
        "sample_rate": sampling_rate,
        "type": "audio",
    }


def concatenate_latents(video_latent, audio_latent):
    concatenated_latent = audio_latent.copy()
    video_noise_mask, audio_noise_mask = video_latent.get("noise_mask"), audio_latent.get("noise_mask")

    if any((video_noise_mask, audio_noise_mask)):
        video_noise_mask = torch.ones_like(video_latent["samples"]) if video_noise_mask is None else video_noise_mask
        audio_noise_mask = torch.ones_like(audio_latent["samples"]) if audio_noise_mask is None else audio_noise_mask
        concatenated_latent["noise_mask"] = NestedTensor((video_noise_mask, audio_noise_mask))

    concatenated_latent["samples"] = NestedTensor((video_latent["samples"], audio_latent["samples"]))

    return concatenated_latent


def build_video_audio_latents(**kwargs):
    video_latent = create_empty_video_latent(**kwargs)
    audio_latent = create_empty_audio_latent(**kwargs)

    return video_latent, audio_latent


def inject_reference_frame(**kwargs):
    vae, latent, image = kwargs.get("video_vae"), kwargs.get("video_latent"), kwargs.get("image_opt")
    samples = latent["samples"]
    _, height_scale_factor, width_scale_factor = (
        vae.downscale_index_formula
    )
    batch, _, latent_frames, latent_height, latent_width = samples.shape
    width = latent_width * width_scale_factor
    height = latent_height * height_scale_factor

    image_height, image_width = image.shape[1:3]

    if image_height != height or image_width != width:
        pixels = utils.common_upscale(
            image.movedim(-1, 1),
            width,
            height,
            kwargs.get("inplace_scale_mode"),
            "center"
        ).movedim(1, -1)
    else:
        pixels = image

    pixel_space = pixels[..., :3]
    encoded = vae.encode(pixel_space)
    samples[:, :, :encoded.shape[2]] = encoded

    latent_frames_mask = torch.ones(
        (batch, 1, latent_frames, 1, 1),
        dtype=torch.float32,
        device=samples.device,
    )
    latent_frames_mask[:, :, :encoded.shape[2]] = 1.0 - kwargs.get("inplace_strength")

    return {"samples": samples, "noise_mask": latent_frames_mask}


class TT_Ltx23LatentsFactoryNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Ltx23LatentsFactoryNode",
            display_name="TT LTX2.3 Latents Factory",
            category=CATEGORY,
            description="",
            inputs=[
                io.Vae.Input("video_vae"),
                io.Vae.Input("audio_vae"),
                io.Image.Input("image_opt", optional=True),
                io.Boolean.Input("use_ref_frame", default=True, label_on="Inplace", label_off="Bypass"),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Combo.Input("aspect_ratio", options=CommonTypes.ASPECT_RATIOS, default="16:9"),
                io.Combo.Input("megapixels", options=CommonTypes.MEGAPIXELS, default="1 MP"),
                io.Combo.Input("orientation", options=CommonTypes.ORIENTATIONS),
                io.Int.Input("length_sec", default=5, min=1, max=20),
                io.Combo.Input("frame_rate", options=CommonTypes.FRAME_RATES, default="24fps"),
                io.Float.Input("inplace_strength", default=1.0, min=0.0, max=1.0),
                io.Combo.Input("inplace_scale_mode", CommonTypes.SCALE_METHODS, default="bicubic"),
                io.Int.Input("batch_size", default=1, min=1, max=64, advanced=True),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
                io.Latent.Output("LATENT_VIDEO"),
                io.Latent.Output("LATENT_AUDIO"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> NodeOutput:
        video_latent, audio_latent = build_video_audio_latents(**kwargs)
        use_ref_frame, image_opt = kwargs.get("use_ref_frame"), kwargs.get("image_opt")

        if use_ref_frame and image_opt:
            kwargs["video_latent"] = video_latent
            video_latent = inject_reference_frame(**kwargs)

        concatenated_latent = concatenate_latents(video_latent, audio_latent)

        return io.NodeOutput(concatenated_latent, video_latent, audio_latent)


__all__ = [
    "TT_LatentFactoryNode",
    "TT_LatentFactoryByModelNode",
    "TT_LatentMultiTransformNode",
    "TT_LatentMultiTransformOnPixelSpaceNode",
    "TT_Ltx23LatentsFactoryNode",
]
