# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from pathlib import Path

import colour
import kornia
import torch
from torch.nn import functional

import folder_paths
from comfy_api.latest import io
from .nodes_image import get_upscale_models, upscale
from .utils import CommonTypes, raise_if

CATEGORY = "TenserTensor/Postproduction"


def apply_film_grain(**kwargs):
    image, seed, scale, strength, saturation, mode, antialias, toe = (
        kwargs.get("image"),
        kwargs.get("seed"),
        kwargs.get("scale"),
        kwargs.get("strength"),
        kwargs.get("saturation"),
        kwargs.get("upscale_mode"),
        kwargs.get("antialias"),
        kwargs.get("toe"),
    )
    timage = image.copy()
    batch, height, width, channels = timage.shape

    if seed is not None:
        torch.manual_seed(seed)

    grain = torch.rand(batch, int(height // scale), int(width // scale), 3)
    ycbcr = kornia.color.rgb_to_ycbcr(grain.movedim(-1, 1)).movedim(1, -1)

    for idx, ksize in enumerate([3, 15, 11]):
        sigma = (ksize / 3.0,) * 2
        kernel_size = (ksize,) * 2
        channel = ycbcr[..., idx:idx + 1].movedim(-1, 1)
        ycbcr[..., idx] = kornia.filters.gaussian_blur2d(
            channel,
            kernel_size=kernel_size,
            sigma=sigma,
            border_type='reflect'
        ).movedim(1, -1).squeeze(-1)

    grain = (kornia.color.ycbcr_to_rgb(ycbcr.movedim(-1, 1)).movedim(1, -1) - 0.5) * strength
    grain[..., 0] *= 2
    grain[..., 2] *= 3
    grain += 1

    mono = grain[..., 1:2].expand(-1, -1, -1, 3)
    grain = grain * saturation + mono * (1 - saturation)

    grain = functional.interpolate(
        grain.movedim(-1, 1),
        size=(height, width),
        mode=mode,
        antialias=antialias if mode in ['bilinear', 'bicubic'] else False
    ).movedim(1, -1)

    base = image[..., :3]
    shadow_lift = 1 - toe
    image[..., :3] = torch.clip(
        (1 - (1 - base) * grain) * shadow_lift + toe,
        0.0, 1.0
    )

    return image


class TT_AddFilmGrainNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_AddFilmGrainNode",
            display_name="TT Add Film Grain",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Float.Input("scale", default=0.25, min=0.05, max=2.0, step=0.05),
                io.Float.Input("strength", default=0.15, min=0.0, max=10.0, step=0.01),
                io.Float.Input("saturation", default=0.2, min=0.0, max=2.0, step=0.01),
                io.Float.Input("toe", default=0.0, min=0.0, max=0.5, step=0.001),
                io.Combo.Input("upscale_mode", options=CommonTypes.SCALE_METHODS, advanced=True),
                io.Boolean.Input("antialias", default=True, label_on="Antialiased", label_off="Raw", advanced=True),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        image = apply_film_grain(**kwargs)

        return io.NodeOutput(image)


def get_lut_files_list():
    base = folder_paths.get_folder_paths("custom_nodes")[0]
    lut_dir = Path(base) / "ComfyUI-TenserTensor" / "lut"
    raise_if(
        not lut_dir.is_dir(),
        FileNotFoundError,
        f"lut dir not found: {lut_dir}"
    )

    files = [file.name for file in lut_dir.glob("*.cube")]

    return lut_dir, sorted(files)


def color_correction(**kwargs):
    image, is_log, lut_dir, lut_file, lut_strength = (
        kwargs.get("image"),
        kwargs.get("colorspace") == "logarithmic",
        kwargs.get("lut_dir"),
        kwargs.get("lut_file"),
        kwargs.get("lut_strength"),
    )

    timage = image.clone()
    orig_np_image = timage.detach().cpu().numpy()
    np_image = orig_np_image.copy()
    device, dtype = timage.device, timage.dtype

    if is_log:
        np_image **= 1 / 2.2

    np_image = colour.read_LUT(str(lut_dir / lut_file)).apply(np_image)

    if is_log:
        np_image **= 2.2

    if lut_strength < 1.0:
        np_image = lut_strength * np_image + (1 - lut_strength) * orig_np_image

    return torch.from_numpy(np_image).to(device, dtype)


class TT_ApplyLutNode(io.ComfyNode):
    LUT_DIR = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        cls.LUT_DIR, LUT_FILES = get_lut_files_list()

        return io.Schema(
            node_id="TT_ApplyLutNode",
            display_name="TT Apply LUT",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Combo.Input("lut_file", options=LUT_FILES),
                io.Float.Input("strength", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Combo.Input("colorspace", options=CommonTypes.COLORSPACES)
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["lut_dir"] = cls.LUT_DIR
        image = color_correction(**kwargs)

        return io.NodeOutput(image)


def adjust_brightness(image, factor, clip_output=True):
    timage = image.movedim(-1, 1)

    return kornia.enhance.adjust_brightness(timage, factor, clip_output).movedim(1, -1)


def adjust_contrast(image, factor, clip_output=True):
    timage = image.movedim(-1, 1)

    return kornia.enhance.adjust_contrast(timage, factor, clip_output).movedim(1, -1)


def adjust_gamma(image, gamma, gain=1.0):
    timage = image.movedim(-1, 1)

    return kornia.enhance.adjust_gamma(timage, gamma, gain).movedim(1, -1)


def adjust_hue(image, factor):
    timage = image.movedim(-1, 1)

    return kornia.enhance.adjust_hue(timage, factor).movedim(1, -1)


def adjust_saturation(image, factor):
    timage = image.movedim(-1, 1)

    return kornia.enhance.adjust_saturation(timage, factor).movedim(1, -1)


def sharpness(image, factor):
    timage = image.movedim(-1, 1)

    return kornia.enhance.sharpness(timage, factor).movedim(1, -1)


def posterize(image, bits):
    timage = image.movedim(-1, 1)

    return kornia.enhance.posterize(timage, bits).movedim(1, -1)


def solarize(image, thresholds=0.5, additions=None):
    timage = image.movedim(-1, 1)

    return kornia.enhance.solarize(timage, thresholds, additions).movedim(1, -1)


def enhance_image(**kwargs):
    image = kwargs.get("image")
    timage = image.clone()

    brightness_factor = kwargs.get("brightness_factor")
    if brightness_factor != 0.0:
        timage = adjust_brightness(timage, brightness_factor)

    contrast_factor = kwargs.get("contrast_factor")
    if contrast_factor != 1.0:
        timage = adjust_contrast(timage, contrast_factor)

    gamma_factor, gamma_gain = kwargs.get("gamma_factor"), kwargs.get("gamma_gain")
    if gamma_factor != 1.0:
        timage = adjust_gamma(timage, gamma_factor, gamma_gain)

    hue_factor = kwargs.get("hue_factor")
    if hue_factor != 0.0:
        timage = adjust_hue(timage, hue_factor)

    saturation_factor = kwargs.get("saturation_factor")
    if saturation_factor != 1.0:
        timage = adjust_saturation(timage, saturation_factor)

    sharpness_factor = kwargs.get("sharpness_factor")
    if sharpness_factor != 0.0:
        timage = sharpness(timage, sharpness_factor)

    posterize_bits = kwargs.get("posterize_bits")
    if posterize_bits != 8:
        timage = posterize(timage, posterize_bits)

    solarize_thresholds = kwargs.get("solarize_thresholds")
    if solarize_thresholds != 1.0:
        timage = solarize(timage, solarize_thresholds)

    return timage


class TT_ImageEnhancerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_ImageEnhancerNode",
            display_name="TT Image Enhancer",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Float.Input("brightness_factor", default=0.0, min=-1.0, max=1.0, step=0.01),
                io.Float.Input("contrast_factor", default=1.0, min=0.0, max=5.0, step=0.01),
                io.Float.Input("gamma_factor", default=1.0, min=0.0, max=3.0, step=0.01),
                io.Float.Input("gamma_gain", default=1.0, min=0.0, max=3.0, step=0.01),
                io.Float.Input("hue_factor", default=0.0, min=-torch.pi, max=torch.pi, step=0.01),
                io.Float.Input("saturation_factor", default=1.0, min=0.0, max=3.0, step=0.01),
                io.Float.Input("sharpness_factor", default=0.0, min=0.0, max=3.0, step=0.01),
                io.Int.Input("posterize_bits", default=8, min=-0, max=8),
                io.Float.Input("solarize_thresholds", default=1.0, min=0.0, max=1.0, step=0.01),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        image = enhance_image(**kwargs)

        return io.NodeOutput(image)


class TT_QuickImageUpscalerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_QuickImageUpscalerNode",
            display_name="TT Quick Image Upscaler",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Combo.Input("upscaler_device", options=CommonTypes.TORCH_DEVICES, advanced=True),
                io.Combo.Input("upscale_model", options=get_upscale_models(), advanced=True),
                io.Int.Input("upscale_tile", default=512, min=128, max=4096, step=64, advanced=True),
                io.Int.Input("upscale_overlap", default=64, min=8, max=256, step=8, advanced=True),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        image = upscale(**kwargs)

        return io.NodeOutput(image)


class TT_PostproductionNode(io.ComfyNode):
    LUT_DIR = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        cls.LUT_DIR, LUT_FILES = get_lut_files_list()

        return io.Schema(
            node_id="TT_PostproductionNode",
            display_name="TT Postproduction",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Boolean.Input("apply_lut", default=True, label_on="Apply LUT", label_off="Skip LUT"),
                io.Combo.Input("lut_file", options=LUT_FILES),
                io.Float.Input("lut_strength", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Combo.Input("colorspace", options=CommonTypes.COLORSPACES),
                io.Boolean.Input("add_film_grain", default=True, label_on="With Grain", label_off="Clean"),
                io.Int.Input("seed", display_name="grain_seed", default=0, min=0, max=0xffffffffffffffff),
                io.Float.Input("scale", display_name="grain_scale", default=0.25, min=0.05, max=2.0, step=0.05),
                io.Float.Input("strength", display_name="grain_strength", default=0.15, min=0.0, max=10.0, step=0.01),
                io.Float.Input("saturation", display_name="grain_saturation", default=0.2, min=0.0, max=2.0, step=0.01),
                io.Float.Input("toe", display_name="grain_toe", default=0.0, min=0.0, max=0.5, step=0.001),
                io.Combo.Input("upscale_mode", display_name="grain_upscale_mode", options=CommonTypes.SCALE_METHODS, advanced=True),
                io.Boolean.Input("antialias", display_name="grain_antialias", default=True, label_on="Antialiased", label_off="Raw", advanced=True),
                io.Boolean.Input("upscale_image", default=True, label_on="Upscale image", label_off="Keep size"),
                io.Combo.Input("upscaler_device", options=CommonTypes.TORCH_DEVICES, advanced=True),
                io.Combo.Input("upscale_model", options=get_upscale_models(), advanced=True),
                io.Int.Input("upscale_tile", default=512, min=128, max=4096, step=64, advanced=True),
                io.Int.Input("upscale_overlap", default=64, min=8, max=256, step=8, advanced=True),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        image = kwargs.get("image")
        kwargs["image"] = image.clone()

        apply_lut, add_film_grain, upscale_image = (
            kwargs.get("apply_lut"),
            kwargs.get("add_film_grain"),
            kwargs.get("upscale_image"),
        )

        if apply_lut:
            kwargs["lut_dir"] = cls.LUT_DIR
            kwargs["image"] = color_correction(**kwargs)

        if add_film_grain:
            kwargs["image"] = apply_film_grain(**kwargs)

        if upscale_image:
            kwargs["image"] = upscale(**kwargs)

        return io.NodeOutput(kwargs.get("image"))


class TT_PostproductionAdvancedNode(io.ComfyNode):
    LUT_DIR = None

    @classmethod
    def define_schema(cls) -> io.Schema:
        cls.LUT_DIR, LUT_FILES = get_lut_files_list()

        return io.Schema(
            node_id="TT_PostproductionAdvancedNode",
            display_name="TT Postproduction (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Boolean.Input("image_enhancer", default=True, label_on="Enhance", label_off="Bypass"),
                io.Float.Input("brightness_factor", default=0.0, min=-1.0, max=1.0, step=0.01),
                io.Float.Input("contrast_factor", default=1.0, min=0.0, max=5.0, step=0.01),
                io.Float.Input("gamma_factor", default=1.0, min=0.0, max=3.0, step=0.01),
                io.Float.Input("gamma_gain", default=1.0, min=0.0, max=3.0, step=0.01),
                io.Float.Input("hue_factor", default=0.0, min=-torch.pi, max=torch.pi, step=0.01),
                io.Float.Input("saturation_factor", default=1.0, min=0.0, max=3.0, step=0.01),
                io.Float.Input("sharpness_factor", default=0.0, min=0.0, max=3.0, step=0.01),
                io.Int.Input("posterize_bits", default=8, min=-0, max=8),
                io.Float.Input("solarize_thresholds", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Boolean.Input("apply_lut", default=True, label_on="Apply LUT", label_off="Bypass"),
                io.Combo.Input("lut_file", options=LUT_FILES),
                io.Float.Input("lut_strength", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Combo.Input("colorspace", options=CommonTypes.COLORSPACES),
                io.Boolean.Input("add_film_grain", default=True, label_on="Add Grain", label_off="Bypass"),
                io.Int.Input("seed", display_name="grain_seed", default=0, min=0, max=0xffffffffffffffff),
                io.Float.Input("scale", display_name="grain_scale", default=0.25, min=0.05, max=2.0, step=0.05),
                io.Float.Input("strength", display_name="grain_strength", default=0.15, min=0.0, max=10.0, step=0.01),
                io.Float.Input("saturation", display_name="grain_saturation", default=0.2, min=0.0, max=2.0, step=0.01),
                io.Float.Input("toe", display_name="grain_toe", default=0.0, min=0.0, max=0.5, step=0.001),
                io.Combo.Input("upscale_mode", display_name="grain_upscale_mode", options=CommonTypes.SCALE_METHODS, advanced=True),
                io.Boolean.Input("antialias", display_name="grain_antialias", default=True, label_on="Antialiased", label_off="Raw", advanced=True),
                io.Boolean.Input("upscale_image", default=True, label_on="Upscale image", label_off="Bypass"),
                io.Combo.Input("upscaler_device", options=CommonTypes.TORCH_DEVICES, advanced=True),
                io.Combo.Input("upscale_model", options=get_upscale_models(), advanced=True),
                io.Int.Input("upscale_tile", default=512, min=128, max=4096, step=64, advanced=True),
                io.Int.Input("upscale_overlap", default=64, min=8, max=256, step=8, advanced=True),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        image = kwargs.get("image")
        kwargs["image"] = image.clone()

        image_enhancer, apply_lut, add_film_grain, upscale_image = (
            kwargs.get("image_enhancer"),
            kwargs.get("apply_lut"),
            kwargs.get("add_film_grain"),
            kwargs.get("upscale_image"),
        )

        if image_enhancer:
            kwargs["image"] = enhance_image(**kwargs)

        if apply_lut:
            kwargs["lut_dir"] = cls.LUT_DIR
            kwargs["image"] = color_correction(**kwargs)

        if add_film_grain:
            kwargs["image"] = apply_film_grain(**kwargs)

        if upscale_image:
            kwargs["image"] = upscale(**kwargs)

        return io.NodeOutput(kwargs.get("image"))


__all__ = [
    "TT_AddFilmGrainNode",
    'TT_ApplyLutNode',
    'TT_ImageEnhancerNode',
    'TT_QuickImageUpscalerNode',
    'TT_PostproductionNode',
    'TT_PostproductionAdvancedNode',
]
