# ComfyUI-TenserTensor

> Eight, sir; seven, sir;  
> Six, sir; five, sir;  
> Four, sir; Three, sir;  
> Two, sir; one!  
> Tenser, said the Tensor.  
> Tenser, said the Tensor.  
> Tension, apprehension,  
> And dissension have begun.

*— Alfred Bester, The Demolished Man*

A collection of custom nodes for ComfyUI that streamline common workflows. The main goal is to reduce visual clutter by
combining frequently used node chains into single, convenient loaders.

## Features

- **Workflow settings nodes** - configure entire workflow parameters (basic and advanced variants)
- **All-in-one model loaders** - load checkpoint, LoRAs, CLIP, and VAE in single nodes
- **Latent factory** - generate latents with aspect ratio, megapixel count, orientation, and type selection (Flux/SDXL)
- **Context nodes** - from Basic to Even Larger Context
    - Basic: combines latent, model, CLIP, VAE, and workflow config into context
    - Others: pass-through nodes that modify specific context values while preserving the rest
- **CLIP text encoders** - context-based and prompt-based encoding with model-specific controls
- **KSamplers** - Different implementations of KSampler for generating images. Accepts all common sampling parameters
  and returns a denoised latent ready for VAE decoding.
- **VAE decoders** - basic, context-based, extended, and two-pass (draft + refinement)
- **Post-production tools** - image adjustments (brightness, contrast, saturation), color correction (apply LUT), film
  grain, upscaler
    - All-in-one post-production node combining all tools
    - Simplified version without adjustments

## Nodes List

### Workflow

#### TT FLUX Workflow Settings

Node for configuring Flux workflow generation parameters.

#### TT FLUX Workflow Settings (Advanced)

Advanced node for configuring Flux workflow generation parameters with separate CLIP-L and T5XXL prompts.

#### TT SDXL Workflow Settings

Node for configuring SDXL workflow generation parameters.

#### TT SDXL Workflow Settings (Advanced)

Advanced SDXL workflow configuration with separate CLIP-L/G prompts and aesthetic scores.

### Latent

#### TT Latent Factory

Generate empty latent images with precise dimension control based on aspect ratio and megapixel count.

Automatically calculates correct dimensions for FLUX and SDXL models, plus separate CLIP conditioning sizes.

### Loaders

#### TT SDXL Models Loader

All-in-one model loader for SDXL workflows with checkpoint merging support.

#### TT SDXL Models Loader (Advanced)

Extended all-in-one model loader for SDXL with checkpoint merging and LoRA support.

#### TT FLUX Models Loader

All-in-one model loader for Flux workflows.

#### TT FLUX Models Loader (Advanced)

Extended all-in-one model loader for Flux with sampling patches, LoRA support, and advanced settings.

### Text Encoder

#### TT CLIP Text Encode FLUX

Flux text encoder with separate CLIP-L and T5-XXL prompt inputs.

#### TT CLIP Text Encode FLUX (Context)

Context-based Flux text encoder that extracts prompts from workflow config.

#### TT CLIP Text Encode SDXL

SDXL text encoder with separate CLIP-L and CLIP-G prompt inputs and conditioning parameters.

#### TT CLIP Text Encode SDXL (Context)

Context-based SDXL text encoder that extracts prompts and parameters from workflow config.

### Samplers

#### TT KSampler
#### TT KSampler (Advanced)
#### TT KSampler (Context)
#### TT KSampler (Two Stages)

### VAE

#### TT VAE Decode (Context)
#### TT VAE Decode (Tiled)
#### TT Vae Encode (Context)
#### TT Vae Encode (Tiled)

### Postproduction

#### TT Apply LUT
#### TT Add Film Grain
#### TT Quick Image Upscaler
#### TT Image Enhancer
#### TT Postproduction
#### TT Postproduction (Advanced)

### Image

#### TT Image Preview / Save

### Context

#### TT Base Context
#### TT Context
#### TT FLUX Large Context
#### TT SDXL Large Context
#### TT Even Larger Context
#### TT Context Set Image
#### TT Context Set Latent
#### TT Context Passthrough
