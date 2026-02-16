from .nodes.context.base_context import TT_BaseContext
from .nodes.context.context import TT_Context
from .nodes.context.context_passthrough import TT_ContextPassthrough
from .nodes.context.even_larger_context import TT_EvenLargerContext
from .nodes.context.large_context_flux import TT_LargeContextFlux
from .nodes.context.large_context_sdxl import TT_LargeContextSdxl
from .nodes.image.image_preview_save import TT_ImagePreviewSave
from .nodes.latent.latent_factory import TT_LatentFactory
from .nodes.loaders.flux_models_loader import TT_FluxModelsLoader
from .nodes.loaders.flux_models_loader_advanced import TT_FluxModelsLoaderAdvanced
from .nodes.loaders.sdxl_models_loader import TT_SdxlModelsLoader
from .nodes.loaders.sdxl_models_loader_advanced import TT_SdxlModelsLoaderAdvanced
from .nodes.postproduction.add_film_grain import TT_AddFilmGrain
from .nodes.postproduction.apply_lut import TT_ApplyLut
from .nodes.postproduction.image_enhancer import TT_ImageEnhancer
from .nodes.postproduction.postproduction import TT_Postproduction
from .nodes.postproduction.postproduction_advanced import TT_PostproductionAdvanced
from .nodes.postproduction.quick_image_upscaler import TT_QuickImageUpscaler
from .nodes.sampling.ksampler import TT_KSampler
from .nodes.sampling.ksampler_advanced import TT_KSamplerAdvanced
from .nodes.sampling.ksampler_context import TT_KSamplerContext
from .nodes.sampling.ksampler_two_stage import TT_KSamplerTwoStage
from .nodes.text_encoders.clip_text_encode_flux import TT_ClipTextEncodeFlux
from .nodes.text_encoders.clip_text_encode_flux_context import TT_ClipTextEncodeFluxContext
from .nodes.text_encoders.clip_text_encode_sdxl import TT_ClipTextEncodeSdxl
from .nodes.text_encoders.clip_text_encode_sdxl_context import TT_ClipTextEncodeSdxlContext
from .nodes.vae.vae_decode_context import TT_VaeDecodeContext
from .nodes.vae.vae_decode_tiled import TT_VaeDecodeTiled
from .nodes.vae.vae_encode_context import TT_VaeEncodeContext
from .nodes.vae.vae_encode_tiled import TT_VaeEncodeTiled
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
    # Image
    "TT_ImagePreviewSave": TT_ImagePreviewSave,
    # Latent
    "TT_LatentFactory": TT_LatentFactory,
    # Loaders
    "TT_SdxlModelsLoader": TT_SdxlModelsLoader,
    "TT_SdxlModelsLoaderAdvanced": TT_SdxlModelsLoaderAdvanced,
    "TT_FluxModelsLoader": TT_FluxModelsLoader,
    "TT_FluxModelsLoaderAdvanced": TT_FluxModelsLoaderAdvanced,
    # Postproduction
    "TT_ApplyLut": TT_ApplyLut,
    "TT_AddFilmGrain": TT_AddFilmGrain,
    "TT_QuickImageUpscaler": TT_QuickImageUpscaler,
    "TT_ImageEnhancer": TT_ImageEnhancer,
    "TT_Postproduction": TT_Postproduction,
    "TT_PostproductionAdvanced": TT_PostproductionAdvanced,
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
    # VAE
    "TT_VaeDecodeContext": TT_VaeDecodeContext,
    "TT_VaeDecodeTiled": TT_VaeDecodeTiled,
    "TT_VaeEncodeContext": TT_VaeEncodeContext,
    "TT_VaeEncodeTiled": TT_VaeEncodeTiled,
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
    "TT_ImagePreviewSave": "TT Image Preview / Save",
    # Latent
    "TT_LatentFactory": "TT Latent Factory",
    # Loaders
    "TT_SdxlModelsLoader": "TT SDXL Models Loader",
    "TT_SdxlModelsLoaderAdvanced": "TT SDXL Models Loader (Advanced)",
    "TT_FluxModelsLoader": "TT FLUX Models Loader",
    "TT_FluxModelsLoaderAdvanced": "TT FLUX Models Loader (Advanced)",
    # Postproduction
    "TT_ApplyLut": "TT Apply LUT",
    "TT_AddFilmGrain": "TT Add Film Grain",
    "TT_QuickImageUpscaler": "TT Quick Image Upscaler",
    "TT_ImageEnhancer": "TT Image Enhancer",
    "TT_Postproduction": "TT Postproduction",
    "TT_PostproductionAdvanced": "TT Postproduction (Advanced)",
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
    # VAE
    "TT_VaeDecodeContext": "TT VAE Decode (Context)",
    "TT_VaeDecodeTiled": "TT VAE Decode (Tiled)",
    "TT_VaeEncodeContext": "TT Vae Encode (Context)",
    "TT_VaeEncodeTiled": "TT Vae Encode (Tiled)",
    # Workflow
    "TT_FluxWorkflowSettings": "TT FLUX Workflow Settings",
    "TT_FluxWorkflowSettingsAdvanced": "TT FLUX Workflow Settings (Advanced)",
    "TT_SdxlWorkflowSettings": "TT SDXL Workflow Settings",
    "TT_SdxlWorkflowSettingsAdvanced": "TT SDXL Workflow Settings (Advanced)",
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
