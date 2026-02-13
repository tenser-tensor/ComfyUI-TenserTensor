from .postproduction_helpers import enhance_image


class TT_ImageEnhancer():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness_factor": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "contrast_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
                "gamma_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "gamma_gain": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "hue_factor": ("FLOAT", {"default": 0.0, "min": -3.14, "max": 3.14, "step": 0.01}),
                "saturation_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "sharpness_factor": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "posterize_bits": ("INT", {"default": 8, "min": 0, "max": 8}),
                "solarize_thresholds": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "enhance_image"
    CATEGORY = "TenserTensor/Postproduction"

    def enhance_image(
            self,
            image,
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
        timage = image.clone()

        timage = enhance_image(
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
        )

        return (timage,)
