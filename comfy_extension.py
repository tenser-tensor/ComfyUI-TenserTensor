# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from typing import override

from comfy_api.latest import ComfyExtension, io

from .nodes_context import NODES as NODES_CONTEXT
from .nodes_controlnet import NODES as NODES_CONTROLNET
from .nodes_detector import NODES as NODES_DETECTOR
from .nodes_image import NODES as NODES_IMAGE
from .nodes_latent import NODES as NODES_LATENT
from .nodes_loaders import NODES as NODES_LOADERS
from .nodes_postproduction import NODES as NODES_POSTPRODUCTION
from .nodes_sampling import NODES as NODES_SAMPLING
from .nodes_text_encoder import NODES as NODES_TEXT_ENCODER
from .nodes_workflow import NODES as NODES_WORKFLOW


class TenserTensorExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            *NODES_CONTEXT,
            *NODES_CONTROLNET,
            *NODES_DETECTOR,
            *NODES_IMAGE,
            *NODES_LATENT,
            *NODES_LOADERS,
            *NODES_POSTPRODUCTION,
            *NODES_SAMPLING,
            *NODES_TEXT_ENCODER,
            *NODES_WORKFLOW,
        ]
