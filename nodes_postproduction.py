# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from typing import override

from comfy_api.latest import ComfyExtension, io

CATEGORY = "TenserTensor/Postproduction"


class TT_AddFilmGrainNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_AddFilmGrainNode",
            display_name="TT Add Film Grain",
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


class TT_ApplyLutNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_ApplyLutNode",
            display_name="TT Apply LUT",
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


class TT_ImageEnhancerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_ImageEnhancerNode",
            display_name="TT Image Enhancer",
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


class TT_QuickImageUpscalerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_QuickImageUpscalerNode",
            display_name="TT Quick Image Upscaler",
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


class TT_PostproductionNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_PostproductionNode",
            display_name="TT Postproduction",
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


class TT_PostproductionAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_PostproductionAdvancedNode",
            display_name="TT Postproduction (Advanced)",
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

class PostproductionNodesExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            # TT_Node,
        ]


async def comfy_entrypoint() -> PostproductionNodesExtension:
    return PostproductionNodesExtension()


# ==============================================================================
# Re-exports for backward compatibility
# ==============================================================================

__all__ = [
    # "TT_Node",
]
