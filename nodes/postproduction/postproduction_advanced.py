# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from folder_paths import get_filename_list

from .postproduction_helpers import get_lut_files_list, color_correction, apply_film_grain, upscale_image, enhance_image


class TT_PostproductionAdvanced():
    LUT_DIR = None

    @classmethod
    def INPUT_TYPES(cls):
        cls.LUT_DIR, LUT_FILES = get_lut_files_list()
        COLORSPACES = ["linear", "logarithmic"]
        UPSCALE_MODES = ["bilinear", "bicubic", "lanczos", "nearest", "area"]
        UPSCALE_MODELS = get_filename_list("upscale_models")
        DEVICES = ["default", "cpu"]

        return {
            "required": {
                "image": ("IMAGE",),
                "image_enhancer": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "brightness_factor": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "contrast_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
                "gamma_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "gamma_gain": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "hue_factor": ("FLOAT", {"default": 0.0, "min": -3.14, "max": 3.14, "step": 0.01}),
                "saturation_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "sharpness_factor": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "posterize_bits": ("INT", {"default": 8, "min": 0, "max": 8}),
                "solarize_thresholds": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "apply_lut": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "lut_file": (LUT_FILES, {"advanced": True}),
                "lut_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "lut_colorspace": (COLORSPACES, {"advanced": True}),
                "add_film_grain": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "grain_seed": (
                    "INT",
                    {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True}
                ),
                "grain_scale": ("FLOAT", {"default": 0.25, "min": 0.25, "max": 2.0, "step": 0.05}),
                "grain_strength": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                "grain_saturation": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.01}),
                "grain_toe": ("FLOAT", {"default": 0.05, "min": -0.2, "max": 0.5, "step": 0.01}),
                "grain_upscale_mode": (UPSCALE_MODES, {"advanced": True}),
                "grain_antialias": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "image_upscaler": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "upscaler_device": (DEVICES, {"advanced": True}),
                "upscale_model_name": (UPSCALE_MODELS, {"advanced": True}),
                "upscaler_tile": ("INT", {"default": 512, "min": 256, "max": 4096, "step": 64}),
                "upscaler_overlap": ("INT", {"default": 64, "min": 0, "max": 256, "step": 8}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "apply_postprocessing"
    CATEGORY = "TenserTensor/Postproduction"

    def apply_postprocessing(self, **kwargs):
        image = kwargs.get("image").clone()

        image_enhancer = kwargs.get("image_enhancer")
        if image_enhancer:
            image = enhance_image(
                timage=image,
                brightness_factor=kwargs.get("brightness_factor"),
                contrast_factor=kwargs.get("contrast_factor"),
                gamma_factor=kwargs.get("gamma_factor"),
                gamma_gain=kwargs.get("gamma_gain"),
                hue_factor=kwargs.get("hue_factor"),
                saturation_factor=kwargs.get("saturation_factor"),
                sharpness_factor=kwargs.get("sharpness_factor"),
                posterize_bits=kwargs.get("posterize_bits"),
                solarize_thresholds=kwargs.get("solarize_thresholds")
            )

        apply_lut = kwargs.get("apply_lut")
        if apply_lut:
            image = color_correction(
                image=image,
                lut_dir=TT_PostproductionAdvanced.LUT_DIR,
                lut_file=kwargs.get("lut_file"),
                strength=kwargs.get("lut_strength"),
                colorspace=kwargs.get("lut_colorspace")
            )

        add_film_grain = kwargs.get("add_film_grain")
        if add_film_grain:
            image = apply_film_grain(
                image=image,
                seed=kwargs.get("grain_seed"),
                scale=kwargs.get("grain_scale"),
                strength=kwargs.get("grain_strength"),
                saturation=kwargs.get("grain_saturation"),
                toe=kwargs.get("grain_toe"),
                mode=kwargs.get("grain_upscale_mode"),
                antialias=kwargs.get("grain_antialias")
            )

        image_upscaler = kwargs.get("image_upscaler")
        if image_upscaler:
            image = upscale_image(
                timage=image,
                device=kwargs.get("upscaler_device"),
                upscale_model_name=kwargs.get("upscale_model_name"),
                tile=kwargs.get("upscaler_tile"),
                overlap=kwargs.get("upscaler_overlap"),
            )

        return (image,)
