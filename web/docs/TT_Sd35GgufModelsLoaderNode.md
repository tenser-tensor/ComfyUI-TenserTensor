## TT SD3.5 GGUF Models Loader *TT_Sd35GgufModelsLoaderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Loads a quantized SD3.5 pipeline from GGUF files. Supports separate GGUF files for the diffusion model and all three text encoders.

### Inputs

| Parameter         | Type  | Required | Description               |
|-------------------|-------|----------|---------------------------|
| `diffusion_model` | COMBO | Yes      | GGUF diffusion model file |
| `clip_l`          | COMBO | Yes      | CLIP-L text encoder file  |
| `clip_g`          | COMBO | Yes      | CLIP-G text encoder file  |
| `t5xxl`           | COMBO | Yes      | T5-XXL text encoder file  |
| `vae_name`        | COMBO | Yes      | VAE file                  |

### Outputs

| Parameter | Type  | Description            |
|-----------|-------|------------------------|
| `MODEL`   | MODEL | Loaded diffusion model |
| `CLIP`    | CLIP  | Loaded CLIP encoders   |
| `VAE`     | VAE   | Loaded VAE             |

### Usage

Place GGUF diffusion model files in `models/diffusion_models_gguf` or `models/diffusion_models`. Place text encoder files in
`models/text_encoders_gguf`, `models/text_encoders` or `models/clip`. VAE is loaded from `models/vae` as a standard safetensors file.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
