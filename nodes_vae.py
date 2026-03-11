# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from typing import override

import torch

from comfy_api.latest import IO, ComfyExtension

TILE_SIZE, OVERLAP = 512, 64


def vae_encode(image, vae, tile_width=TILE_SIZE, tile_height=TILE_SIZE, overlap=OVERLAP):
    samples = vae.encode_tiled(
        image,
        tile_x=tile_width,
        tile_y=tile_height,
        overlap=overlap
    )

    return {"samples": samples}


def vae_decode(latent, vae, tile_width=TILE_SIZE, tile_height=TILE_SIZE, overlap=OVERLAP):
    samples = latent["samples"]

    compression = vae.spacial_compression_decode()
    images = vae.decode_tiled(
        samples,
        tile_x=tile_width // compression,
        tile_y=tile_height // compression,
        overlap=overlap // compression
    )

    return images


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

class VaeNodesExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[IO.ComfyNode]]:
        return [
            # TT_Node,
        ]


async def comfy_entrypoint() -> VaeNodesExtension:
    return VaeNodesExtension()


# ==============================================================================
# Re-exports for backward compatibility
# ==============================================================================

__all__ = [
    # "TT_Node",
]
