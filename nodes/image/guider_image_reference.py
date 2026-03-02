# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import os

import folder_paths as FP
from node_helpers import conditioning_set_values

from ..image.image_helpers import load_image, resize_image_to_megapixels
from ...lib.common import CommonTypes

UPSCALE_METHODS = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
TILE_SIZE, OVERLAP = 512, 64


class TT_GuiderImageReference():
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = FP.get_input_directory()
        files = FP.filter_files_content_types(
            [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))], ["image"]
        )

        return {
            "required": {
                "vae": ("VAE",),
                "guider": ("GUIDER",),
                "megapixels": (CommonTypes.MEGAPIXELS,),
                "upscale_method": (UPSCALE_METHODS, {"default": "bicubic", "advanced": True}),
                "dimension_step": ("INT", {"default": 1, "min": 1, "max": 10000, "advanced": True}),
                "image": (sorted(files), {"image_upload": True}),
            },
        }

    RETURN_TYPES = ("VAE", "GUIDER",)
    RETURN_NAMES = ("VAE", "GUIDER",)
    FUNCTION = "update_latent"
    CATEGORY = "TenserTensor/Deprecated/Image"

    def update_latent(self, vae, guider, megapixels, upscale_method, dimension_step, image):
        timage, _ = load_image(image)
        scaled = resize_image_to_megapixels(timage, upscale_method, megapixels, dimension_step)

        samples = vae.encode_tiled(
            scaled,
            tile_x=TILE_SIZE,
            tile_y=TILE_SIZE,
            overlap=OVERLAP
        )

        conditioning = guider.get_conds()

        if conditioning is not None:
            conditioning = conditioning_set_values(conditioning, {"reference_latents": [samples]}, append=True)
            guider.set_conds(conditioning)
        else:
            raise ValueError("ERROR: Guider has no conditioning")

        return (vae, guider,)
