from folder_paths import get_filename_list

from .postproduction_helpers import upscale_image


class TT_QuickImageUpscaler():
    @classmethod
    def INPUT_TYPES(cls):
        DEVICES = ["default", "cpu"]
        UPSCALE_MODELS = get_filename_list("upscale_models")

        return {
            "required": {
                "image": ("IMAGE",),
                "device": (DEVICES, {"advanced": True}),
                "upscale_model_name": (UPSCALE_MODELS, {"advanced": True}),
                "tile": ("INT", {"default": 512, "min": 256, "max": 4096, "step": 64}),
                "overlap": ("INT", {"default": 64, "min": 0, "max": 256, "step": 8}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "upscale_image"
    CATEGORY = "TenserTensor/Postproduction"


    def upscale_image(self, image, device, upscale_model_name, tile, overlap):
        timage = image.clone()

        return (upscale_image(
            timage=timage,
            device=device,
            upscale_model_name=upscale_model_name,
            tile=tile,
            overlap=overlap,
        ),)
