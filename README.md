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

A collection of custom nodes for ComfyUI that streamline common workflows. The main goal is to reduce visual clutter by combining frequently used node
chains into single, convenient loaders.

> [!IMPORTANT]  
> ⚠️ **Note:** The pack is currently undergoing refactoring and migration to ComfyUI API V3. Some nodes are marked as deprecated and will be removed
> in a future major release. Please check node descriptions for migration guidance.

## Features

- **Workflow settings** — configure global workflow parameters for FLUX, SDXL, and SD3.5
- **Model loaders** — all-in-one loaders for checkpoint, LoRA, CLIP, and VAE; GGUF support for FLUX2 and SD3.5
- **Context nodes** — pass pipeline state between nodes as a single context object
- **Latent factory** — create latents with aspect ratio, megapixel, and orientation selection; automatic format detection from model
- **CLIP text encoders** — prompt encoding with model-specific controls for FLUX, SDXL, and SD3.5
- **Samplers** — KSampler variants including guided sampling with Guider/Sigmas support and step-by-step latent preview
- **Image tools** — load, resize, upscale, preview, save, and reference images for ControlNet
- **VAE** — encode and decode with tiled and context-based variants
- **Post-production** — brightness, contrast, saturation, LUT, film grain, and upscaling
-

## Installation

> [!IMPORTANT]  
> Ensure your ComfyUI version is recent enough to properly support custom operations when loading UNET-only models.

### 1. Via Git Clone (recommended)

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/tenser-tensor/ComfyUI-TenserTensor
```

### 2. Via ComfyUI-Manager

* Open ComfyUI-Manager
* Click "Install Custom Nodes"
* Search for: TenserTensor
* Install → Restart ComfyUI

### 3. Via comfy-cli

```bash
comfy node install tenser-tensor/ComfyUI-TenserTensor
```

Restart ComfyUI after installation.

## Acknowledgments

This project uses GGUF file handling code from [City96](https://github.com/city96).

Great thanks and appreciation for your excellent work!

[ComfyUI-GGUF on Github](https://github.com/city96/ComfyUI-GGUF)

## Additional

> [!NOTE]  
> ⚠️ **Custom Type Compatibility Notice:** The custom data types `TT_CONTEXT` and `TT_WORKFLOW_CONFIG` are **proprietary to this node pack** and are
> not compatible with native ComfyUI nodes or third-party nodes.  
> These types can only be connected to inputs and outputs within the **ComfyUI-TenserTensor** pack. Attempting to pass them to external nodes will
> result in a type mismatch error.
 
> [!NOTE]  
> **For GGUF users:** ComfyUI does not scan for GGUF files by default.  
> Place your files according to the structure below — the node pack registers these folders automatically.   

```
📂 ComfyUI/  
├── 📂 models/  
│   ├── 📂 diffusion_models/  
│   │      └── # GGUF diffusion models (main location)  
│   ├── 📂 unet/  
│   │      └── # GGUF diffusion models (alternative location, deprecated)  
│   ├── 📂 diffusion_models_gguf/  
│   │      └── # GGUF diffusion models (recommended)  
│   ├── 📂 text_encoders/  
│   │      └── # Text encoders: CLIP-L, CLIP-G, T5-XXL (safetensors or GGUF, main location)  
│   ├── 📂 clip/  
│   │      └── # Text encoders (alternative location, deprecated)  
│   ├── 📂 text_encoders_gguf/  
│   │      └── # Text encoders (recommended)  
│   ├── 📂 loras/  
│   │      └── # LoRA files  
│   └── 📂 vae/  
│          └── # VAE files (safetensors)  
```

> [!TIP]  
> You can download Flux.2-dev along with additional models (CLIP, VAE) via the link below:  
> [Comfy-Org/flux2-dev](https://huggingface.co/Comfy-Org/flux2-dev/tree/main/split_files)

---

_(c) 2026 TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)_
