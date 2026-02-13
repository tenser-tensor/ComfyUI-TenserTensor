from .postproduction_helpers import apply_film_grain


class TT_AddFilmGrain():
    @classmethod
    def INPUT_TYPES(cls):
        UPSCALE_MODES = ["bilinear", "bicubic", "lanczos", "nearest", "area"]

        return {
            "required": {
                "image": ("IMAGE",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "scale": ("FLOAT", {"default": 0.25, "min": 0.25, "max": 2.0, "step": 0.05}),
                "strength": ("FLOAT", {"default": 0.15, "min": 0.0, "max": 10.0, "step": 0.01}),
                "saturation": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 2.0, "step": 0.01}),
                "toe": ("FLOAT", {"default": 0.0, "min": -0.2, "max": 0.5, "step": 0.001}),
                "upscale_mode": (UPSCALE_MODES, {"advanced": True}),
                "antialias": ("BOOLEAN", {"default": False, "label_on": "Enabled", "label_off": "Disabled"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "apply_film_grain"
    CATEGORY = "TenserTensor/Postproduction"

    def apply_film_grain(self, **kwargs):
        return (apply_film_grain(
            image=kwargs.get("image").clone(),
            seed=kwargs.get("seed"),
            scale=kwargs.get("scale"),
            strength=kwargs.get("strength"),
            saturation=kwargs.get("saturation"),
            toe=kwargs.get("toe"),
            mode=kwargs.get("upscale_mode"),
            antialias=kwargs.get("antialias"),
        ),)
