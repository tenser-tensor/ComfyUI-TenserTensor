import fnmatch
import os
import random
import string as S
from datetime import datetime

import folder_paths as FP
import numpy as NP
from PIL import Image

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
