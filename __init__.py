# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .comfy_extension import TenserTensorExtension

WEB_DIRECTORY = "./web"


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

async def comfy_entrypoint() -> TenserTensorExtension:
    return TenserTensorExtension()
