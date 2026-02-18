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

[Nodes List](NODES.md)