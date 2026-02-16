from pathlib import Path

import colour
import comfy.utils as U
import kornia
import torch
import torch.nn.functional as F
from comfy import model_management
from folder_paths import get_folder_paths, get_filename_list, get_full_path_or_raise
from spandrel import ModelLoader, ImageModelDescriptor


def get_lut_files_list():
    base = get_folder_paths("custom_nodes")[0]
    lut_dir = Path(base) / "ComfyUI-TenserTensor" / "lut"

    if not lut_dir.is_dir():
        raise FileNotFoundError(f"lut dir not found: {lut_dir}")

    files = [file.name for file in lut_dir.glob("*.cube")]

    return lut_dir, sorted(files)


def color_correction(image, lut_dir, lut_file, strength, colorspace):
    is_log = colorspace == "logarithmic"
    device, dtype = image.device, image.dtype
    image = image.detach().cpu().numpy()
    retval = image.copy()
    if is_log:
        retval **= 1 / 2.2
    retval = colour.read_LUT(str(lut_dir / lut_file)).apply(retval)
    if is_log:
        retval **= 2.2
    if strength < 1.0:
        retval = strength * retval + (1 - strength) * image

    return torch.from_numpy(retval).to(device, dtype)


def apply_film_grain(image, seed, scale, strength, saturation, toe, mode, antialias):
    batch, height, width, channels = image.shape
    image = image.detach()
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

    grain = F.interpolate(
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


def _load_upscale_model(upscale_model_name):
    model_path = get_full_path_or_raise("upscale_models", upscale_model_name)

    try:
        state_dict = U.load_torch_file(model_path, safe_load=True)
    except Exception as e:
        raise RuntimeError(f"Failed to load model file {model_path}: {e}")

    state_dict = U.state_dict_prefix_replace(state_dict, {"module.": ""})
    upscale_model = ModelLoader().load_from_state_dict(state_dict).eval()

    if not isinstance(upscale_model, ImageModelDescriptor):
        raise TypeError(f"Expected ImageModelDescriptor, got {type(upscale_model).__name__}")

    return upscale_model


def upscale_image(timage, device, upscale_model_name, tile, overlap):
    upscale_device = model_management.get_torch_device() if device == "default" else torch.device("cpu")
    upscale_model = _load_upscale_model(upscale_model_name)

    iimage = timage.movedim(-1, 1).to(upscale_device)
    batch, channels, height, width = iimage.shape

    BUFFER_FACTOR = 384.0

    model_mem = model_management.module_size(upscale_model.model)
    tile_mem = (tile * tile * 3) * iimage.element_size() * max(upscale_model.scale, 1) * BUFFER_FACTOR
    total_mem = model_mem + tile_mem + iimage.nelement() * iimage.element_size()
    model_management.free_memory(total_mem, upscale_device)
    upscale_model.to(upscale_device)

    try:
        while True:
            try:
                steps = batch * U.get_tiled_scale_steps(
                    width,
                    height,
                    tile_x=tile,
                    tile_y=tile,
                    overlap=overlap
                )
                pbar = U.ProgressBar(steps)
                simage = U.tiled_scale(
                    iimage,
                    upscale_model,
                    tile_x=tile,
                    tile_y=tile,
                    overlap=overlap,
                    upscale_amount=upscale_model.scale,
                    pbar=pbar
                )
                break
            except model_management.OOM_EXCEPTION as e:
                pbar = None
                tile //= 2
                if tile < 128:
                    raise e
    finally:
        if upscale_device.type != "cpu":
            upscale_model.to("cpu")

    return torch.clamp(simage.movedim(1, -1), min=0.0, max=1.0)


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

def enhance_image(
        timage,
        brightness_factor,
        contrast_factor,
        gamma_factor,
        gamma_gain,
        hue_factor,
        saturation_factor,
        sharpness_factor,
        posterize_bits,
        solarize_thresholds
):
    if brightness_factor != 0.0:
        timage = adjust_brightness(timage, brightness_factor)

    if contrast_factor != 1.0:
        timage = adjust_contrast(timage, contrast_factor)

    if gamma_factor != 1.0:
        timage = adjust_gamma(timage, gamma_factor, gamma_gain)

    if hue_factor != 0.0:
        timage = adjust_hue(timage, hue_factor)

    if saturation_factor != 1.0:
        timage = adjust_saturation(timage, saturation_factor)

    if sharpness_factor != 0.0:
        timage = sharpness(timage, sharpness_factor)

    if posterize_bits != 8:
        timage = posterize(timage, posterize_bits)

    if solarize_thresholds != 1.0:
        timage = solarize(timage, solarize_thresholds)

    return timage
