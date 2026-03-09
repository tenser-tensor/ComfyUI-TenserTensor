## TT GGUF Models Loader *TT_GgufModelsLoaderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Loads a complete GGUF-quantized pipeline (diffusion model, text encoder, and VAE) in a single node.

### Inputs

| Parameter         | Type  | Required | Description                                 |
|-------------------|-------|----------|---------------------------------------------|
| `diffusion_model` | COMBO | Yes      | GGUF-quantized diffusion model file         |
| `clip`            | COMBO | Yes      | GGUF-quantized text encoder file            |
| `vae_name`        | COMBO | Yes      | VAE model file for image encoding/decoding  |

### Outputs

| Parameter | Type  | Description                         |
|-----------|-------|-------------------------------------|
| `MODEL`   | MODEL | Loaded GGUF diffusion model         |
| `CLIP`    | CLIP  | Loaded GGUF text encoder            |
| `VAE`     | VAE   | Loaded VAE                          |

### Usage

Convenience node for loading a GGUF-quantized pipeline in one step. Designed for use with quantized model
files that reduce VRAM requirements. Select the GGUF diffusion model, GGUF text encoder, and VAE from
their respective dropdowns. LoRA loading is supported at this stage; bypass LoRA is not applied.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
