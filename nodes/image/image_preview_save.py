# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .image_helpers import store, preview


class TT_ImagePreviewSave():
    @classmethod
    def INPUT_TYPES(cls):
        FILENAME_FORMATS = ["name-###", "date-name-###", "name-datetime"]
        IMAGE_FORMATS = ["PNG", "JPEG", "WEBP"]

        return {
            "required": {
                "image": ("IMAGE",),
                "save_image": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "filename_prefix": ("STRING", {"default": "tenser-tensor"}),
                "filename_format": (FILENAME_FORMATS, {"default": "name-###", "advanced": True}),
                "subfolder": ("STRING", {"default": "", "advanced": True}),
                "image_format": (IMAGE_FORMATS, {"default": "PNG", "advanced": True}),
                "image_quality": ("INT", {"default": 100, "min": 0, "max": 100, "advanced": True}),
                "compression_level": ("INT", {"default": 9, "min": 0, "max": 9, "advanced": True}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True
    FUNCTION = "preview_save_image"
    CATEGORY = "TenserTensor/Image"

    def preview_save_image(
            self,
            image,
            save_image,
            filename_prefix,
            filename_format,
            subfolder,
            image_format,
            image_quality,
            compression_level
    ):
        if save_image:
            retval = store(
                image,
                filename_prefix,
                filename_format,
                subfolder,
                image_format,
                image_quality,
                compression_level
            )
        else:
            retval = preview(image, filename_prefix)

        return {"ui": {"images": retval}}
