## TT SDXL Models Loader (Advanced) *TT_SdxlModelsLoaderAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended SDXL loader with built-in LoRA support and VAE device and dtype configuration. Loads up to four LoRAs in a single node alongside the main
pipeline.

### Inputs

| Parameter        | Type  | Required | Description                                      |
|------------------|-------|----------|--------------------------------------------------|
| `primary_ckpt`   | COMBO | Yes      | Primary checkpoint file                          |
| `secondary_ckpt` | COMBO | No       | Secondary checkpoint for merging, `None` to skip |
| `primary_weight` | FLOAT | No       | Merge weight for primary checkpoint, default 1.0 |
| `clip_l`         | COMBO | Yes      | CLIP-L text encoder file                         |
| `clip_g`         | COMBO | Yes      | CLIP-G text encoder file                         |
| `clip_device`    | COMBO | No       | Device for CLIP inference, default `default`     |
| `lora_name_1-4`  | COMBO | No       | LoRA files, up to four                           |
| `strength_1-4`   | FLOAT | No       | LoRA strength, default 1.0, range -10.0 to 10.0  |
| `vae_name`       | COMBO | Yes      | VAE file                                         |
| `vae_device`     | COMBO | No       | Device for VAE inference, default `default`      |
| `vae_dtype`      | COMBO | No       | VAE data type                                    |

### Outputs

| Parameter | Type  | Description            |
|-----------|-------|------------------------|
| `MODEL`   | MODEL | Loaded diffusion model |
| `CLIP`    | CLIP  | Loaded CLIP encoders   |
| `VAE`     | VAE   | Loaded VAE             |

### Usage

Identical to TT SDXL Models Loader with added LoRA and VAE configuration. Unused LoRA slots are ignored. Negative LoRA strength values invert the
effect.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
