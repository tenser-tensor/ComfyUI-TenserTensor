# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from torch import bfloat16, float16, float32, float8_e4m3fn, float8_e5m2

from comfy.latent_formats import SDXL, Flux, Flux2, SD3


class CommonTypes():
    ASPECT_RATIOS = ["1:1", "4:3", "3:2", "16:9", "21:9"]
    CLIP_MULTIPLIERS = ["1x", "2x", "4x"]
    COLORSPACES = ["linear", "logarithmic"]
    FILENAME_FORMATS = ["name-###", "date-name-###", "name-datetime"]
    FORMAT_EXT = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp", }
    FRAME_RATES = ["12fps", "24fps", "25fps", "30fps", "48fps", "50fps", "60fps"]
    IMAGE_TAES = ["taesd", "taesdxl", "taesd3", "taef1"]
    LATENT_DIMENSION_STEP = 64
    MAX_SAMPLING_RES = 4096
    MEGAPIXELS = ["0.25 MP", "0.5 MP", "1 MP", "2 MP", "4 MP", "8 MP"]
    MIN_SAMPLING_RES = 256
    MODEL_DTYPES = {"fp8_e4m3fn": float8_e4m3fn, "fp8_e4m3fn_fast": float8_e4m3fn, "fp8_e5m2": float8_e5m2}
    MODEL_TYPES = {"FLUX1.D": Flux, "FLUX2.D": Flux2, "SDXL": SDXL, "SD3.X": SD3}
    ORIENTATIONS = ["landscape", "portrait"]
    ROTATE_ANGLES = ["90°", "180°", "270°"]
    SCALE_FACTORS = ["0.25x", "0.5x", "1x", "2x", "4x", "8x"]
    SCALE_METHODS = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]
    TORCH_DEVICE_CPU = "cpu"
    TORCH_DEVICES = ["default", "cpu"]
    TORCH_DTYPES = {"bfloat16": bfloat16, "float16": float16, "float32": float32}
    VIDEO_TAES = ["taehv", "lighttaew2_2", "lighttaew2_1", "lighttaehy1_5"]


def raise_if(cond: bool, exception: type[Exception], msg: str = "") -> None:
    if cond:
        raise exception(f"ERROR: {msg}")


def raise_unless(cond: bool, exception: type[Exception], msg: str = "") -> None:
    if not cond:
        raise exception(f"ERROR: {msg}")
