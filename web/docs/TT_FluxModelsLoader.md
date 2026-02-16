## TT FLUX Models Loader *TT_FluxModelsLoader*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

All-in-one model loader for Flux workflows.

### Inputs

| Parameter     | Type       | Required | Description                                     |
|---------------|------------|----------|-------------------------------------------------|
| `ckpt_name`   | CHECKPOINT | Yes      | Flux checkpoint to load                         |
| `clip_l`      | STRING     | Yes      | CLIP-L text encoder model                       |
| `t5xxl`       | STRING     | Yes      | T5-XXL text encoder model                       |
| `clip_device` | STRING     | Yes      | Device for CLIP ("default" or "cpu") - advanced |
| `vae_name`    | VAE        | Yes      | VAE model to load                               |

### Outputs

| Parameter | Type  | Description                              |
|-----------|-------|------------------------------------------|
| `MODEL`   | MODEL | Loaded Flux model                        |
| `CLIP`    | CLIP  | Combined CLIP-L and T5-XXL text encoders |
| `VAE`     | VAE   | Loaded VAE                               |

### Usage

Load all Flux model components in one place. Combines CLIP-L and T5-XXL encoders into a dual CLIP for Flux's text
conditioning system.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
