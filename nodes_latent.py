# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import math

import torch

from comfy import model_management, latent_formats, utils, sample
from comfy.nested_tensor import NestedTensor
from comfy_api.latest import io
from .utils import (
    CommonTypes,
)

CATEGORY = "TenserTensor/Latent"


# ==============================================================================
# Helper classes — data structures and base types
# ==============================================================================

class RandomNoise:
    def __init__(self, seed):
        self.seed = seed

    def generate_noise(self, input_latent):
        latent_image = input_latent["samples"]
        batch_idx = input_latent["batch_index"] if "batch_index" in input_latent else None

        return sample.prepare_noise(latent_image, self.seed, batch_idx)


# ==============================================================================
# Helper functions — pipeline utilities and loaders
# ==============================================================================

def calculate_dimensions(total_pixels: int, ratio_w: int, ratio_h: int) -> tuple[int, int]:
    latent_dimension_step = CommonTypes.LATENT_DIMENSION_STEP
    height = int(math.sqrt(total_pixels * ratio_h / ratio_w))
    width = int(height * ratio_w / ratio_h)
    width = round(width / latent_dimension_step) * latent_dimension_step
    height = round(height / latent_dimension_step) * latent_dimension_step

    return width, height


def calculate_dimensions_from_megapixels(megapixels: str, aspect_ratio: str, orientation: str) -> tuple[int, int]:
    total_pixels = int(float(megapixels.split()[0]) * 1_000_000)
    ratio_parts = aspect_ratio.split(':')
    ratio_w, ratio_h = (
        (int(ratio_parts[0]), int(ratio_parts[1]))
        if orientation == "landscape"
        else (int(ratio_parts[1]), int(ratio_parts[0]))
    )
    width, height = calculate_dimensions(total_pixels, ratio_w, ratio_h)

    return width, height


def calc_total_length(**kwargs):
    length_sec, frame_rate, batch_size = (
        kwargs.get("length_sec"),
        kwargs.get("frame_rate"),
        kwargs.get("batch_size"),
    )
    fps = int(frame_rate.replace('fps', ''))
    frames_count = length_sec * fps
    total_length = ((frames_count - 1) // 8) * 8 + 1

    return total_length, fps


def inject_reference_frame(video_latent, **kwargs):
    video_vae, use_ref_frame = kwargs.get("video_vae"), kwargs.get("use_ref_frame")
    samples = video_latent["samples"]
    _, height_scale_factor, width_scale_factor = video_vae.downscale_index_formula
    batch, _, latent_frames, latent_height, latent_width = samples.shape
    width = latent_width * width_scale_factor
    height = latent_height * height_scale_factor

    image, inplace_strength, inplace_scale_mode = (
        use_ref_frame.get("image"),
        use_ref_frame.get("inplace_strength"),
        use_ref_frame.get("inplace_scale_mode")
    )
    image_height, image_width = image.shape[1:3]

    if image_height != height or image_width != width:
        pixels = utils.common_upscale(
            image.movedim(-1, 1),
            width,
            height,
            inplace_scale_mode,
            "center"
        ).movedim(1, -1)
    else:
        pixels = image

    pixel_space = pixels[..., :3]
    encoded = video_vae.encode(pixel_space)
    samples[:, :, :encoded.shape[2]] = encoded

    latent_frames_mask = torch.ones(
        (batch, 1, latent_frames, 1, 1),
        dtype=torch.float32,
        device=samples.device,
    )
    latent_frames_mask[:, :, :encoded.shape[2]] = 1.0 - inplace_strength

    return {"samples": samples, "noise_mask": latent_frames_mask}


def create_empty_video_latent(**kwargs):
    megapixels = kwargs.get("megapixels")
    width, height = calculate_dimensions_from_megapixels(
        megapixels,
        kwargs.get("aspect_ratio"),
        kwargs.get("orientation")
    )
    total_length, fps = calc_total_length(**kwargs)
    fmt = latent_formats.LTXAV()
    generator = torch.Generator().manual_seed(kwargs.get("seed"))
    video_samples = torch.randn(
        kwargs.get("batch_size"),
        fmt.latent_channels,
        total_length,
        height // fmt.spacial_downscale_ratio,
        width // fmt.spacial_downscale_ratio,
        generator=generator,
        device=model_management.intermediate_device()
    )

    return {"samples": video_samples}, total_length, fps, width, height


def create_empty_audio_latent(total_length, fps, **kwargs):
    audio_vae = kwargs.get("audio_vae")

    channels = audio_vae.latent_channels
    audio_freq = audio_vae.latent_frequency_bins
    sampling_rate = int(audio_vae.sample_rate)
    num_audio_latents = audio_vae.num_of_latents_from_frames(total_length, fps)

    generator = torch.Generator().manual_seed(kwargs.get("seed"))
    audio_samples = torch.randn(
        kwargs.get("batch_size"),
        channels,
        num_audio_latents,
        audio_freq,
        generator=generator,
        device=model_management.intermediate_device()
    )

    return {
        "samples": audio_samples,
        "sample_rate": sampling_rate,
        "type": "audio",
    }


def concatenate_latents(video_latent, audio_latent):
    concatenated_latent = audio_latent.copy()
    video_noise_mask, audio_noise_mask = video_latent.get("noise_mask"), audio_latent.get("noise_mask")

    if video_noise_mask is not None or audio_noise_mask is not None:
        video_noise_mask = torch.ones_like(video_latent["samples"]) if video_noise_mask is None else video_noise_mask
        audio_noise_mask = torch.ones_like(audio_latent["samples"]) if audio_noise_mask is None else audio_noise_mask
        concatenated_latent["noise_mask"] = NestedTensor((video_noise_mask, audio_noise_mask))

    concatenated_latent["samples"] = NestedTensor((video_latent["samples"], audio_latent["samples"]))

    return concatenated_latent


def prepare_multimodal_latents(**kwargs):
    use_ref_frame, seed, noise_seed, megapixels = (
        kwargs.get("use_ref_frame"),
        kwargs.get("seed"),
        kwargs.get("noise_seed"),
        kwargs.get("megapixels")
    )

    video_latent, width, height, total_length, fps = create_empty_video_latent(**kwargs)

    if use_ref_frame.get("use_ref_frame") == "Inplace":
        video_latent = inject_reference_frame(video_latent, **kwargs)

    audio_latent = create_empty_audio_latent(total_length, fps, **kwargs)
    concatenated_latent = concatenate_latents(video_latent, audio_latent)
    random_noise = RandomNoise(noise_seed)

    return (
        concatenated_latent,
        video_latent,
        audio_latent,
        random_noise,
        seed,
        noise_seed,
        megapixels,
        total_length,
        fps,
        width,
        height,
    )


# ==============================================================================
# Node classes — ComfyUI node definitions
# ==============================================================================


class TT_LtxvLatentFactoryNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LtxvLatentFactoryNode",
            display_name="TT LTXV Latent Factory",
            category=CATEGORY,
            description="",
            inputs=[
                io.Vae.Input("video_vae"),
                io.Vae.Input("audio_vae"),
                io.DynamicCombo.Input("use_ref_frame", options=[
                    io.DynamicCombo.Option("Inplace", [
                        io.Image.Input("image"),
                        io.Float.Input("inplace_strength", default=0.7, min=0.0, max=1.0),
                        io.Combo.Input("inplace_scale_mode", CommonTypes.SCALE_METHODS, default="bicubic"),
                    ]),
                    io.DynamicCombo.Option("Bypass", []),
                ]),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("noise_seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Combo.Input("aspect_ratio", options=CommonTypes.ASPECT_RATIOS),
                io.Combo.Input("megapixels", options=CommonTypes.MEGAPIXELS),
                io.Combo.Input("orientation", options=CommonTypes.ORIENTATIONS),
                io.Int.Input("length_sec", default=5, min=1, max=20),
                io.Combo.Input("frame_rate", options=CommonTypes.FRAME_RATES, default="24fps"),
                io.Int.Input("batch_size", default=1, min=1, max=64),
            ],
            outputs=[
                io.Latent.Output(display_name="CONCATENATED_LATENT"),
                io.Latent.Output(display_name="VIDEO_LATENT"),
                io.Latent.Output(display_name="AUDIO_LATENT"),
                io.Noise.Output(display_name="RANDOM_NOISE"),
                io.Int.Output(display_name="SEED"),
                io.Int.Output(display_name="NOISE_SEED"),
                io.String.Output(display_name="MEGAPIXELS"),
                io.Int.Output(display_name="TOTAL_LENGTH"),
                io.Int.Output(display_name="FPS"),
                io.Int.Output(display_name="WIDTH"),
                io.Int.Output(display_name="HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        args = prepare_multimodal_latents(**kwargs)

        return io.NodeOutput(*args)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

NODES = [
    TT_LtxvLatentFactoryNode,
]
