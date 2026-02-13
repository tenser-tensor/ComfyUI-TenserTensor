## TT SDXL Models Loader *TT_SdxlModelsLoader*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

All-in-one model loader for SDXL workflows with checkpoint merging support.

### Inputs

| Parameter        | Type         | Required | Description                                                    |
|------------------|--------------|----------|----------------------------------------------------------------|
| `primary_ckpt`   | CHECKPOINT   | Yes      | Primary SDXL checkpoint to load                                |
| `secondary_ckpt` | CHECKPOINT   | Yes      | Secondary checkpoint to merge (select "None" to skip)          |
| `primary_weight` | FLOAT        | Yes      | Weight for primary checkpoint in merge (0.0-1.0, default: 1.0) |
| `clip_l`         | TEXT_ENCODER | Yes      | CLIP-L text encoder model                                      |
| `clip_g`         | TEXT_ENCODER | Yes      | CLIP-G text encoder model                                      |
| `clip_device`    | STRING       | Yes      | Device for CLIP ("default" or "cpu") - advanced                |
| `vae_name`       | VAE          | Yes      | VAE model to load                                              |

### Outputs

| Parameter | Type  | Description                               |
|-----------|-------|-------------------------------------------|
| `MODEL`   | MODEL | Loaded (and optionally merged) SDXL model |
| `CLIP`    | CLIP  | Combined CLIP-L and CLIP-G text encoders  |
| `VAE`     | VAE   | Loaded VAE                                |

### Usage

Use this node to load all SDXL model components in one place. Optionally merge two checkpoints by selecting a secondary
checkpoint and adjusting the primary_weight (1.0 = 100% primary, 0.5 = 50/50 mix, 0.0 = 100% secondary).

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
