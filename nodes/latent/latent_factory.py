# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .latent_helpers import create_empty_latent
from ...lib.common import CommonTypes

ASPECT_RATIOS = ["1:1", "4:3", "3:2", "16:9", "21:9"]
ORIENTATIONS = ["landscape", "portrait"]
MODEL_TYPES = ["FLUX1.D", "FLUX2.D", "SDXL"]
CLIP_MULTIPLIERS = ["1x", "2x", "4x"]


class TT_LatentFactory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff},),
                "noise_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff},),
                "aspect_ratio": (ASPECT_RATIOS,),
                "megapixels": (CommonTypes.MEGAPIXELS,),
                "orientation": (ORIENTATIONS,),
                "model_type": (MODEL_TYPES,),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64, "advanced": True},),
                "clip_multiplier": (CLIP_MULTIPLIERS, {"advanced": True},)
            }
        }

    RETURN_TYPES = ("LATENT", "NOISE", "INT", "INT", CommonTypes.MEGAPIXELS, "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("LATENT", "RANDOM_NOISE", "SEED", "NOISE_SEED", "MEGAPIXELS", "WIDTH", "HEIGHT", "TARGET_WIDTH", "TARGET_HEIGHT")
    FUNCTION = "create_latent"
    CATEGORY = "TenserTensor/Latent"

    def create_latent(self, **kwargs):
        return create_empty_latent(**kwargs)
