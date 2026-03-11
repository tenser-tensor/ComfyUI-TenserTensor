## TT FLUX Models Loader *TT_FluxModelsLoaderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Loads all components of the FLUX pipeline (diffusion model, text encoders, and VAE) in a single node.

### Inputs

| Parameter         | Type  | Required | Description                                    |
|-------------------|-------|----------|------------------------------------------------|
| `diffusion_model` | COMBO | Yes      | FLUX diffusion model checkpoint file           |
| `clip_l`          | COMBO | Yes      | CLIP-L text encoder file                       |
| `t5xxl`           | COMBO | Yes      | T5-XXL text encoder file                       |
| `clip_device`     | COMBO | Yes      | Device for CLIP inference (default: "default") |
| `vae_name`        | COMBO | Yes      | VAE model file for image encoding/decoding     |

### Outputs

| Parameter | Type  | Description                 |
|-----------|-------|-----------------------------|
| `MODEL`   | MODEL | Loaded FLUX diffusion model |
| `CLIP`    | CLIP  | Loaded CLIP+T5 text encoder |
| `VAE`     | VAE   | Loaded VAE                  |

### Usage

Convenience node for loading the complete FLUX pipeline in one step. Select the diffusion model,
both text encoders (CLIP-L and T5-XXL), and VAE from their respective dropdowns. Use `clip_device`
to offload text encoders to a specific device if needed. LoRA loading is not applied at this stage.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
