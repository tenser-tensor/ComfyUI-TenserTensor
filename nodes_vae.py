# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from typing import override

import torch

from comfy_api.latest import io, ComfyExtension

CATEGORY="TenserTensor/VAE"

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


class TT_KSamplerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerNode",
            display_name="TT_KSampler",
            category=CATEGORY,
            description="",
            inputs=[

            ],
            outputs=[

            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        raise NotImplementedError


class TT_KSamplerAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerAdvancedNode",
            display_name="TT_KSampler (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[

            ],
            outputs=[

            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        raise NotImplementedError


class TT_KSamplerContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerContextNode",
            display_name="TT_KSampler (Context)",
            category=CATEGORY,
            description="",
            inputs=[

            ],
            outputs=[

            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        raise NotImplementedError


class TT_KSamplerTwoStageNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerTwoStageNode",
            display_name="TT_KSampler (Two Stage)",
            category=CATEGORY,
            description="",
            inputs=[

            ],
            outputs=[

            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        raise NotImplementedError


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
