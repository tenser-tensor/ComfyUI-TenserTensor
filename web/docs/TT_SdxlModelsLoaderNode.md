## TT SDXL Models Loader *TT_SdxlModelsLoaderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Loads SDXL model, CLIP encoders, and VAE in a single node. Supports optional model merging with a secondary checkpoint.

### Inputs

| Parameter        | Type  | Required | Description                                      |
|------------------|-------|----------|--------------------------------------------------|
| `primary_ckpt`   | COMBO | Yes      | Primary checkpoint file                          |
| `secondary_ckpt` | COMBO | No       | Secondary checkpoint for merging, `None` to skip |
| `primary_weight` | FLOAT | No       | Merge weight for primary checkpoint, default 1.0 |
| `clip_l`         | COMBO | Yes      | CLIP-L text encoder file                         |
| `clip_g`         | COMBO | Yes      | CLIP-G text encoder file                         |
| `clip_device`    | COMBO | No       | Device for CLIP inference, default `default`     |
| `vae_name`       | COMBO | Yes      | VAE file                                         |

### Outputs

| Parameter | Type  | Description            |
|-----------|-------|------------------------|
| `MODEL`   | MODEL | Loaded diffusion model |
| `CLIP`    | CLIP  | Loaded CLIP encoders   |
| `VAE`     | VAE   | Loaded VAE             |

### Usage

Select a primary checkpoint and separate CLIP-L, CLIP-G encoder files. To merge two checkpoints, select a secondary checkpoint and adjust
`primary_weight` — at 1.0 only the primary is used, at 0.5 both are weighted equally.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
