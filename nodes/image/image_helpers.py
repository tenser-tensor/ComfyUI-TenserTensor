import os
import random
import string as S
from datetime import datetime

import folder_paths as FP
import numpy as NP
from PIL import Image


def _save(
        images,
        prefix,
        output_path,
        filename_format=None,
        image_format="PNG",
        quality=50,
        compress_level=4
):
    height, width = images[0].shape[:2]
    save_path, filename, counter, subfolder, _ = FP.get_save_image_path(
        prefix, output_path, height, width
    )

    retval = list()
    for (idx, image) in enumerate(images):
        img_np = 255. * image.cpu().numpy()
        timage = Image.fromarray(NP.clip(img_np, 0, 255).astype(NP.uint8))

        match filename_format:
            case "name-###":
                filename = f"{filename}-{counter:05}"
            case "date-name-###":
                date = datetime.now().strftime("%Y-%m-%d")
                filename = f"{date}-{filename}-{counter:05}"
            case "name-datetime":
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = f"{filename}-{timestamp}"
            case _:
                pass

        params = {}
        match image_format:
            case "PNG":
                filename += ".png"
                params["compress_level"] = compress_level
            case "JPEG":
                filename += ".jpg"
                params["quality"] = quality
            case "WEBP":
                filename += ".webp"
                params["quality"] = quality

        timage.save(os.path.join(save_path, filename), format=image_format, **params)

        retval.append({
            "filename": filename,
            "subfolder": subfolder,
            "type": "temp" if prefix.startswith("tmp") else "output"
        })
        counter += 1

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
    prefix = os.path.join(subfolder, filename_prefix)

    return _save(
        images=image,
        prefix=prefix,
        output_path=output_folder,
        filename_format=filename_format,
        image_format=image_format,
        quality=image_quality,
        compress_level=compress_level
    )


def preview(image, filename_prefix):
    temp_dir = FP.get_temp_directory()
    rand = "".join(random.choices(S.ascii_lowercase, k=5))
    prefix = f"tmp-{filename_prefix}-{rand}"

    return _save(
        images=image,
        prefix=prefix,
        output_path=temp_dir,
    )
