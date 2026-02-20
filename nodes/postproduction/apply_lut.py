# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .postproduction_helpers import get_lut_files_list, color_correction


class TT_ApplyLut:
    LUT_DIR = None

    @classmethod
    def INPUT_TYPES(cls):
        cls.LUT_DIR, LUT_FILES = get_lut_files_list()
        COLORSPACES = ["linear", "logarithmic"]

        return {
            "required": {
                "image": ("IMAGE",),
                "lut_file": (LUT_FILES, {"advanced": True}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "colorspace": (COLORSPACES, {"advanced": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "apply_lut"
    CATEGORY = "TenserTensor/Postproduction"

    def apply_lut(self, image, lut_file, strength, colorspace):
        return (
            color_correction(
                image.clone(),
                TT_ApplyLut.LUT_DIR,
                lut_file,
                strength,
                colorspace
            ),
        )
