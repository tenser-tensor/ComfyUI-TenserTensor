from .nodes.context.base_context import TT_BaseContext
from .nodes.context.context import TT_Context
from .nodes.context.context_passthrough import TT_ContextPassthrough
from .nodes.context.even_larger_context import TT_EvenLargerContext
from .nodes.context.large_context_flux import TT_LargeContextFlux
from .nodes.context.large_context_sdxl import TT_LargeContextSdxl
from .nodes.latent.latent_factory import TT_LatentFactory
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
    # Workflow
    "TT_FluxWorkflowSettings": "TT FLUX Workflow Settings",
    "TT_FluxWorkflowSettingsAdvanced": "TT FLUX Workflow Settings (Advanced)",
    "TT_SdxlWorkflowSettings": "TT SDXL Workflow Settings",
    "TT_SdxlWorkflowSettingsAdvanced": "TT SDXL Workflow Settings (Advanced)",
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
