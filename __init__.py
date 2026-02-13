from .nodes.context.base_context import TT_BaseContext
from .nodes.context.context import TT_Context
from .nodes.context.context_passthrough import TT_ContextPassthrough
from .nodes.context.even_larger_context import TT_EvenLargerContext
from .nodes.context.large_context_flux import TT_LargeContextFlux
from .nodes.context.large_context_sdxl import TT_LargeContextSdxl
from .nodes.latent.latent_factory import TT_LatentFactory
from .nodes.loaders.sdxl_models_loader import TT_SdxlModelsLoader
from .nodes.loaders.sdxl_models_loader_advanced import TT_SdxlModelsLoaderAdvanced
from .nodes.sampling.ksampler import TT_KSampler
from .nodes.sampling.ksampler_advanced import TT_KSamplerAdvanced
from .nodes.sampling.ksampler_context import TT_KSamplerContext
from .nodes.sampling.ksampler_two_stage import TT_KSamplerTwoStage
from .nodes.text_encoders.clip_text_encode_flux import TT_ClipTextEncodeFlux
from .nodes.text_encoders.clip_text_encode_flux_context import TT_ClipTextEncodeFluxContext
from .nodes.text_encoders.clip_text_encode_sdxl import TT_ClipTextEncodeSdxl
from .nodes.text_encoders.clip_text_encode_sdxl_context import TT_ClipTextEncodeSdxlContext
from .nodes.workflow.flux_workfow_settings import TT_FluxWorkflowSettings
from .nodes.workflow.flux_workfow_settings_advanced import TT_FluxWorkflowSettingsAdvanced
from .nodes.workflow.sdxl_workfow_settings import TT_SdxlWorkflowSettings
from .nodes.workflow.sdxl_workfow_settings_advanced import TT_SdxlWorkflowSettingsAdvanced

NODE_CLASS_MAPPINGS = {
    # Context
    "TT_BaseContext": TT_BaseContext,
    "TT_Context": TT_Context,
    "TT_LargeContextFlux": TT_LargeContextFlux,
    "TT_LargeContextSdxl": TT_LargeContextSdxl,
    "TT_EvenLargerContext": TT_EvenLargerContext,
    # Context Passthrough
    "TT_ContextPassthrough": TT_ContextPassthrough,
    # Latent
    "TT_LatentFactory": TT_LatentFactory,
    # Loaders
    "TT_SdxlModelsLoader": TT_SdxlModelsLoader,
    "TT_SdxlModelsLoaderAdvanced": TT_SdxlModelsLoaderAdvanced,
    # Samplers
    "TT_KSampler": TT_KSampler,
    "TT_KSamplerAdvanced": TT_KSamplerAdvanced,
    "TT_KSamplerContext": TT_KSamplerContext,
    "TT_KSamplerTwoStage": TT_KSamplerTwoStage,
    # Text Encoder
    "TT_ClipTextEncodeFlux": TT_ClipTextEncodeFlux,
    "TT_ClipTextEncodeFluxContext": TT_ClipTextEncodeFluxContext,
    "TT_ClipTextEncodeSdxl": TT_ClipTextEncodeSdxl,
    "TT_ClipTextEncodeSdxlContext": TT_ClipTextEncodeSdxlContext,
    # Workflow
    "TT_FluxWorkflowSettings": TT_FluxWorkflowSettings,
    "TT_FluxWorkflowSettingsAdvanced": TT_FluxWorkflowSettingsAdvanced,
    "TT_SdxlWorkflowSettings": TT_SdxlWorkflowSettings,
    "TT_SdxlWorkflowSettingsAdvanced": TT_SdxlWorkflowSettingsAdvanced,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Context
    "TT_BaseContext": "TT Base Context",
    "TT_Context": "TT Context",
    "TT_LargeContextFlux": "TT FLUX Large Context",
    "TT_LargeContextSdxl": "TT SDXL Large Context",
    "TT_EvenLargerContext": "TT Even Larger Context",
    # Context Passthrough
    "TT_ContextPassthrough": "TT Context Passthrough",
    # Latent
    "TT_LatentFactory": "TT Latent Factory",
    # Loaders
    "TT_SdxlModelsLoader": "TT SDXL Models Loader",
    "TT_SdxlModelsLoaderAdvanced": "TT SDXL Models Loader (Advanced)",
    # Samplers
    "TT_KSampler": "TT KSampler",
    "TT_KSamplerAdvanced": "TT KSampler (Advanced)",
    "TT_KSamplerContext": "TT KSampler (Context)",
    "TT_KSamplerTwoStage": "TT KSampler (Two Stages)",
    # Text Encoder
    "TT_ClipTextEncodeFlux": "TT CLIP Text Encode FLUX",
    "TT_ClipTextEncodeFluxContext": "TT CLIP Text Encode FLUX (Context)",
    "TT_ClipTextEncodeSdxl": "TT CLIP Text Encode SDXL",
    "TT_ClipTextEncodeSdxlContext": "TT CLIP Text Encode SDXL (Context)",
    # Workflow
    "TT_FluxWorkflowSettings": "TT FLUX Workflow Settings",
    "TT_FluxWorkflowSettingsAdvanced": "TT FLUX Workflow Settings (Advanced)",
    "TT_SdxlWorkflowSettings": "TT SDXL Workflow Settings",
    "TT_SdxlWorkflowSettingsAdvanced": "TT SDXL Workflow Settings (Advanced)",
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
