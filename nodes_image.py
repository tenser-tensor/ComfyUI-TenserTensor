# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)
import math
import os
from pathlib import Path
from typing import override

import numpy
import torch
from PIL import Image, ImageOps, ImageSequence

import folder_paths
from comfy import model_management, utils
from comfy_api.latest import ComfyExtension, IO, ui
from comfy_api.latest._io import UploadType
from node_helpers import pillow
from .nodes_latent import MEGAPIXELS

CATEGORY = "TenserTensor/Image"
RESIZE_METHODS = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]


def align_to_step(size, scale_factor, dimension_step):
    return round(size * scale_factor / dimension_step) * dimension_step


# crop = "center" / "disabled"
def resize_image(timage, to_width, to_height, upscale_method, dimension_step=1, crop="disabled"):
    samples = timage.movedim(-1, 1)
    orig_height, orig_width = samples.shape[2:]
    scale_factor = max(to_width / orig_width, to_height / orig_height)
    to_width = align_to_step(orig_width, scale_factor, dimension_step)
    to_height = align_to_step(orig_height, scale_factor, dimension_step)

    return utils.common_upscale(samples, int(to_width), int(to_height), upscale_method, crop).movedim(1, -1)


def resize_image_to_megapixels(timage, resize_method, megapixels, dimension_step=1):
    mp_value = float(megapixels.split()[0])
    total_pixels = int(mp_value * 1_000_000)
    samples = timage.movedim(-1, 1)
    orig_height, orig_width = samples.shape[2:]
    scale_factor = math.sqrt(total_pixels / (orig_width * orig_height))
    to_width = align_to_step(orig_width, scale_factor, dimension_step)
    to_height = align_to_step(orig_height, scale_factor, dimension_step)

    return utils.common_upscale(samples, int(to_width), int(to_height), resize_method, "disabled").movedim(1, -1)


def load_image(filename, create_mask, device=None):
    tdevice = torch.device(device) if device is not None else model_management.get_torch_device()
    path = folder_paths.get_annotated_filepath(filename)
    pil_image = pillow(Image.open, path)

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

        if create_mask:
            alpha = numpy.zeros((height, width,), dtype=numpy.float32)
            if 'A' in pil_frame.getbands():
                alpha = numpy.array(pil_frame.getchannel('A'), dtype=numpy.float32) / 255.0
            elif pil_frame.mode == 'P' and 'transparency' in pil_frame.info:
                alpha = numpy.array(pil_frame.convert('RGBA').getchannel('A'), dtype=numpy.float32) / 255.0
            tmask = torch.from_numpy(1.0 - alpha).to(tdevice)
            masks.append(tmask)

        rgb_frame = pil_frame.convert("RGB")
        np_image = numpy.array(rgb_frame, dtype=numpy.float32) / 255.0
        timage = torch.from_numpy(np_image)[None].to(tdevice)

        images.append(timage)

        if pil_image.format == "MPO":
            break

    if len(images) == 0:
        raise ValueError(f"ERROR: No frames found in {path}")

    o_image = torch.cat(images, dim=0) if len(images) > 1 else images[0]

    match len(masks):
        case 0:
            o_mask = torch.zeros((1, height, width), dtype=torch.float32)
        case 1:
            o_mask = masks[0]
        case _:
            o_mask = torch.cat(masks, dim=0)

    return o_image, o_mask


class TT_ImageLoaderResizerNode(IO.ComfyNode):
    @classmethod
    def get_image_files(cls):
        return sorted([
            f.name for f in os.scandir(folder_paths.get_input_directory())
            if f.is_file() and Path(f.name).suffix.lower() in (".png", ".jpg", ".webp", ".bmp")
        ])

    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="TT_ImageLoaderResizerNode",
            display_name="TT Image Loader / Resizer",
            category=CATEGORY,
            description="",
            inputs=[
                IO.Boolean.Input("resize_image", default=False, label_on="Scale", label_off="Keep"),
                IO.Combo.Input("resize_method", options=RESIZE_METHODS, advanced=True),
                IO.Int.Input("dimension_step", default=1, min=1, max=256, advanced=True),
                IO.Combo.Input("megapixels", options=MEGAPIXELS, advanced=True),
                IO.Boolean.Input("create_mask", default=False, label_on="Mask", label_off="None"),
                IO.Combo.Input("image", options=cls.get_image_files(), upload=UploadType.image)
            ],
            outputs=[
                IO.Image.Output(display_name="IMAGE"),
                IO.Mask.Output(display_name="MASK"),
            ],
        )

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        path = folder_paths.get_annotated_filepath(kwargs.get("image"))
        resize = kwargs.get("resize_image")
        result = {
            "image": path + str(os.path.getmtime(path)),
            "resize_image": resize,
            "resize_method": kwargs.get("resize_method"),
            "dimension_step": kwargs.get("dimension_step"),
            "create_mask": kwargs.get("create_mask"),
        }

        if resize:
            result["megapixels"] = kwargs.get("megapixels")

        return result

    @classmethod
    def validate_inputs(cls, **kwargs) -> bool | str:
        path = folder_paths.get_annotated_filepath(kwargs.get("image"))
        if not os.path.isfile(path):
            return f"Image file not found: {path}"

        return True

    @classmethod
    def execute(cls, **kwargs) -> IO.NodeOutput:
        timage, tmask = load_image(kwargs.get("image"), kwargs.get("create_mask"))
        if kwargs.get("resize_image"):
            resize_method, megapixels, dimension_step = kwargs.get("resize_method"), kwargs.get("megapixels"), kwargs.get("dimension_step")
            timage = resize_image_to_megapixels(
                timage,
                resize_method,
                megapixels,
                dimension_step
            )
            tmask = resize_image_to_megapixels(
                tmask,
                resize_method,
                megapixels,
                dimension_step
            )

        return IO.NodeOutput(timage, tmask, ui=ui.PreviewImage(timage, cls=cls))


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

class ImageNodesExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[IO.ComfyNode]]:
        return [
            TT_ImageLoaderResizerNode,
        ]


async def comfy_entrypoint() -> ImageNodesExtension:
    return ImageNodesExtension()


# ==============================================================================
# Re-exports for backward compatibility
# ==============================================================================

__all__ = [
    "TT_ImageLoaderResizerNode",
]
