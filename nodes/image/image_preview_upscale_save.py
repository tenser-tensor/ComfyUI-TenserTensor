# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)
import folder_paths as FP

from .image_helpers import store, preview
from ..postproduction.postproduction_helpers import upscale_image as upscale


class TT_ImagePreviewUpscaleSave():
    @classmethod
    def INPUT_TYPES(cls):
        FILENAME_FORMATS = ["name-###", "date-name-###", "name-datetime"]
        IMAGE_FORMATS = ["PNG", "JPEG", "WEBP"]
        DEVICES = ["default", "cpu"]
        UPSCALE_MODELS = FP.get_filename_list("upscale_models")

        return {
            "required": {
                "image": ("IMAGE",),
                "save_image": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "filename_prefix": ("STRING", {"default": "tenser-tensor"}),
                "filename_format": (FILENAME_FORMATS, {"advanced": True, "default": "name-###"}),
                "subfolder": ("STRING", {"default": "", "advanced": True}),
                "image_format": (IMAGE_FORMATS, {"advanced": True, "default": "PNG"}),
                "image_quality": ("INT", {"default": 100, "min": 0, "max": 100, "advanced": True}),
                "compression_level": ("INT", {"default": 9, "min": 0, "max": 9, "advanced": True}),
                "upscale_image": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "upscaler_device": (DEVICES, {"advanced": True}),
                "upscale_model_name": (UPSCALE_MODELS, {"advanced": True}),
                "tile": ("INT", {"default": 512, "min": 256, "max": 4096, "step": 64, "advanced": True}),
                "overlap": ("INT", {"default": 64, "min": 0, "max": 256, "step": 8, "advanced": True}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True
    FUNCTION = "preview_upscale_save_image"
    CATEGORY = "TenserTensor/Deprecated/Image"

    def preview_upscale_save_image(self, **kwargs):
        image = kwargs.get("image")
        timage = image.clone()

        upscale_image = kwargs.get("upscale_image")
        if upscale_image:
            timage = upscale(
                timage=timage,
                device=kwargs.get("upscaler_device"),
                upscale_model_name=kwargs.get("upscale_model_name"),
                tile=kwargs.get("tile"),
                overlap=kwargs.get("overlap")
            )

        save_image = kwargs.get("save_image")
        if save_image:
            timage = store(
                image=timage,
                filename_prefix=kwargs.get("filename_prefix"),
                subfolder=kwargs.get("subfolder"),
                filename_format=kwargs.get("filename_format"),
                image_format=kwargs.get("image_format"),
                image_quality=kwargs.get("image_quality"),
                compress_level=kwargs.get("compression_level"),
            )
        else:
            timage = preview(
                image=timage,
                filename_prefix=kwargs.get("filename_prefix"),
            )

        return {"ui": {"images": timage}}
