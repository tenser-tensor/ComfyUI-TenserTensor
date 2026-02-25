# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import fnmatch
import math
import os
import random
import string as S
from datetime import datetime

import folder_paths as FP
import numpy
import numpy as NP
import torch
from PIL import Image, ImageOps, ImageSequence
from comfy import model_management as MM
from comfy import utils as U
from node_helpers import pillow

FORMAT_EXT = {
    "PNG": ".png",
    "JPEG": ".jpg",
    "WEBP": ".webp",
}


class InvalidSavePathError(Exception):
    pass


def _build_filename(save_path, filename_mask):
    count = sum(1 for f in os.scandir(save_path) if fnmatch.fnmatch(f.name, filename_mask)) + 1

    return filename_mask.replace("*", f"{count:05}")


def _build_save_path(output_path, subfolder, filename_prefix, filename_format, image_format):
    save_path = os.path.join(output_path, subfolder)
    if os.path.commonpath((output_path, os.path.abspath(save_path))) != output_path:
        raise InvalidSavePathError("Saving image outside the output folder is not allowed.")

    os.makedirs(save_path, exist_ok=True)

    ext = FORMAT_EXT[image_format]

    filename = ""
    match filename_format:
        case "name-###":
            filename = _build_filename(save_path, f"{filename_prefix}-*{ext}")
        case "date-name-###":
            date = datetime.now().strftime("%Y-%m-%d")
            filename = _build_filename(save_path, f"{date}-{filename_prefix}-*{ext}")
        case "name-datetime":
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"{filename_prefix}-{timestamp}{ext}"
        case _:
            filename = f"{filename_prefix}{ext}"

    return save_path, filename


def _store_image(
        images,
        filename_prefix,
        output_path,
        subfolder,
        filename_format,
        image_format,
        quality,
        compress_level
):
    retval = list()
    for image in images:
        img_np = 255. * image.cpu().numpy()
        timage = Image.fromarray(NP.clip(img_np, 0, 255).astype(NP.uint8))
        save_path, filename = _build_save_path(
            output_path, subfolder, filename_prefix, filename_format, image_format
        )
        params = {"compress_level": compress_level} if image_format == "PNG" else {"quality": quality}
        timage.save(os.path.join(save_path, filename), format=image_format, **params)

        retval.append({
            "filename": filename,
            "subfolder": subfolder,
            "type": "temp" if filename_prefix.startswith("tmp") else "output"
        })

    return retval


def store(
        image,
        filename_prefix,
        filename_format,
        subfolder,
        image_format,
        image_quality,
        compress_level
):
    output_folder = FP.get_output_directory()

    return _store_image(
        images=image,
        filename_prefix=filename_prefix,
        output_path=output_folder,
        subfolder=subfolder,
        filename_format=filename_format,
        image_format=image_format,
        quality=image_quality,
        compress_level=compress_level
    )


def preview(image, filename_prefix):
    temp_dir = FP.get_temp_directory()
    rand = "".join(random.choices(S.ascii_lowercase, k=5))
    prefix = f"tmp-{filename_prefix}-{rand}"

    return _store_image(
        images=image,
        filename_prefix=prefix,
        output_path=temp_dir,
    )


def load_image(image_filename, device=None):
    tdevice = MM.get_torch_device() if device == None else torch.device("cpu")

    image_path = FP.get_annotated_filepath(image_filename)
    pil_image = pillow(Image.open, image_path)

    images, masks = [], []
    width, height = None, None

    for frame in ImageSequence.Iterator(pil_image):
        pil_frame = pillow(ImageOps.exif_transpose, frame)

        if pil_frame.mode == "I":
            pil_frame = pil_frame.point(lambda i: i * (1 / 255))

        if len(images) == 0:
            width, height = pil_frame.size

        if pil_frame.size != (width, height,):
            continue

        alpha = numpy.zeros((height, width,), dtype=numpy.float32)
        if 'A' in pil_frame.getbands():
            alpha = numpy.array(pil_frame.getchannel('A'), dtype=numpy.float32) / 255.0
        elif pil_frame.mode == 'P' and 'transparency' in pil_frame.info:
            alpha = numpy.array(pil_frame.convert('RGBA').getchannel('A'), dtype=numpy.float32) / 255.0

        tmask = torch.from_numpy(1.0 - alpha).to(tdevice)

        rgb_frame = pil_frame.convert("RGB")
        np_image = numpy.array(rgb_frame, dtype=numpy.float32) / 255.0
        timage = torch.from_numpy(np_image)[None].to(tdevice)

        images.append(timage)
        masks.append(tmask)

        if pil_image.format == "MPO":
            break

    if len(images) == 0:
        raise ValueError(f"ERROR: No frames found in {image_path}")

    oimage = torch.cat(images, dim=0) if len(images) > 1 else images[0]
    omask = torch.cat(masks, dim=0) if len(masks) > 1 else masks[0]

    return oimage, omask


def _align_to_step(size, scale_factor, dimension_step):
    return round(size * scale_factor / dimension_step) * dimension_step


# crop = "center" / "disabled"
def resize_image(timage, to_width, to_height, upscale_method, dimension_step=1, crop="disabled"):
    samples = timage.movedim(-1, 1)
    orig_height, orig_width = samples.shape[2:]
    scale_factor = max(to_width / orig_width, to_height / orig_height)
    to_width = _align_to_step(orig_width, scale_factor, dimension_step)
    to_height = _align_to_step(orig_height, scale_factor, dimension_step)

    return U.common_upscale(samples, int(to_width), int(to_height), upscale_method, crop).movedim(1, -1)


def resize_image_to_megapixels(timage, upscale_method, megapixels, dimension_step=1):
    mp_value = float(megapixels.split()[0])
    total_pixels = int(mp_value * 1_000_000)
    samples = timage.movedim(-1, 1)
    orig_height, orig_width = samples.shape[2:]
    scale_factor = math.sqrt(total_pixels / (orig_width * orig_height))
    to_width = _align_to_step(orig_width, scale_factor, dimension_step)
    to_height = _align_to_step(orig_height, scale_factor, dimension_step)

    return U.common_upscale(samples, int(to_width), int(to_height), upscale_method, "disabled").movedim(1, -1)
