# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from comfy_api.latest import ComfyExtension, io
from .nodes_context import *
from .nodes_controlnet import *
from .nodes_detector import *
from .nodes_image import *
from .nodes_latent import *
from .nodes_loaders import *
from .nodes_postproduction import *
from .nodes_sampling import *
from .nodes_text_encoder import *
from .nodes_vae import *
from .nodes_workflow import *


class TenserTensorExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            # Context V3 Nodes
            TT_BaseContextNode,
            TT_BaseContextFlux2Node,
            TT_ContextPassthroughNode,
            TT_ContextNode,
            TT_ContextFlux2Node,
            TT_ContextSetGuiderNode,
            TT_ContextSetImageNode,
            TT_ContextSetLatentNode,
            TT_ContextExtractEncoderFlux2Node,
            TT_ContextExtractGuidedSamplerFlux2Node,
            TT_ContextExtractVaeNode,
            TT_ContextExtractImageNode,
            # ControlNet V3 Nodes
            TT_Flux2ApplyControlNetNode,
            TT_Flux2ApplyControlNetAdvancedNode,
            # Detector V3 Nodes
            TT_CannyEdgeDetectorNode,
            # Image V3 Nodes
            TT_ImageLoaderResizerNode,
            TT_ImagePreviewSaveNode,
            TT_ImagePreviewUpscaleSaveNode,
            TT_GuiderImageReferenceNode,
            # Latent V3 Nodes
            TT_LatentFactoryNode,
            TT_LatentFactoryByModelNode,
            TT_LatentMultiTransformNode,
            TT_LatentMultiTransformOnPixelSpaceNode,
            TT_Ltx23LatentsFactoryNode,
            # Loaders V3 Nodes
            TT_SdxlModelsLoaderNode,
            TT_SdxlModelsLoaderAdvancedNode,
            TT_FluxModelsLoaderNode,
            TT_FluxModelsLoaderAdvancedNode,
            TT_Flux2GgufModelsLoaderNode,
            TT_Flux2GgufModelsLoaderAdvancedNode,
            TT_Sd35GgufModelsLoaderNode,
            TT_Sd35GgufModelsLoaderAdvancedNode,
            TT_Ltx23GgufModelsLoaderNode,
            TT_Ltx23GgufModelsLoaderAdvancedNode,
            # Postproduction V3 Nodes
            TT_AddFilmGrainNode,
            TT_ApplyLutNode,
            TT_ImageEnhancerNode,
            TT_QuickImageUpscalerNode,
            TT_PostproductionNode,
            TT_PostproductionAdvancedNode,
            # Samplers V3 Nodes
            TT_KSamplerNode,
            TT_KSamplerAdvancedNode,
            TT_KSamplerContextNode,
            TT_KSamplerTwoStageNode,
            TT_GuidedKSamplerNode,
            TT_GuidedUpscaleKSamplerNode,
            # Text Encoder V3 Nodes
            TT_SdxlClipTextEncoderNode,
            TT_SdxlClipTextEncoderContextNode,
            TT_Flux1ClipTextEncoderNode,
            TT_Flux1ClipTextEncoderContextNode,
            TT_Flux2TextEncoderNode,
            TT_Flux2TextEncoderContextNode,
            TT_Sd35TextEncoderNode,
            TT_Sd35TextEncoderContextNode,
            TT_Ltx23TextEncoderNode,
            # VAE V3 Nodes
            TT_VaeDecodeTiledNode,
            TT_VaeDecodeContextNode,
            TT_VaeEncodeTiledNode,
            TT_VaeEncodeContextNode,
            # Video V3 Nodes
            # Workflow V3 Nodes
            TT_SdxlWorkflowSettingsNode,
            TT_SdxlWorkflowSettingsAdvancedNode,
            TT_FluxWorkflowSettingsNode,
            TT_FluxWorkflowSettingsAdvancedNode,
            TT_Flux2WorkflowSettingsNode,
            TT_Flux2WorkflowSettingsAdvancedNode,
            TT_Sd35GgufWorkflowSettingsNode,
            TT_Sd35GgufWorkflowSettingsAdvancedNode,
            TT_Ltx23GgufWorkflowSettingsNode,
            TT_Ltx23GgufWorkflowSettingsAdvancedNode,
        ]
