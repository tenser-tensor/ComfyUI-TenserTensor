## TT_SdxlModelsLoaderAdvanced

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended all-in-one model loader for SDXL with checkpoint merging and LoRA support.

### Inputs

| Parameter        | Type         | Required | Description                                                     |
|------------------|--------------|----------|-----------------------------------------------------------------|
| `primary_ckpt`   | CHECKPOINT   | Yes      | Primary SDXL checkpoint to load                                 |
| `secondary_ckpt` | CHECKPOINT   | Yes      | Secondary checkpoint to merge (select "None" to skip)           |
| `primary_weight` | FLOAT        | Yes      | Weight for primary checkpoint in merge (0.0-1.0, default: 1.0)  |
| `clip_l`         | TEXT_ENCODER | Yes      | CLIP-L text encoder model                                       |
| `clip_g`         | TEXT_ENCODER | Yes      | CLIP-G text encoder model                                       |
| `clip_device`    | STRING       | Yes      | Device for CLIP ("default" or "cpu") - advanced                 |
| `lora_name_1`    | LORA         | Yes      | First LoRA to apply (select "None" to skip)                     |
| `strength_1`     | FLOAT        | Yes      | Strength for first LoRA (-10.0 to 10.0, default: 1.0)           |
| `lora_name_2`    | LORA         | Yes      | Second LoRA to apply (select "None" to skip)                    |
| `strength_2`     | FLOAT        | Yes      | Strength for second LoRA (-10.0 to 10.0, default: 1.0)          |
| `lora_name_3`    | LORA         | Yes      | Third LoRA to apply (select "None" to skip)                     |
| `strength_3`     | FLOAT        | Yes      | Strength for third LoRA (-10.0 to 10.0, default: 1.0)           |
| `lora_name_4`    | LORA         | Yes      | Fourth LoRA to apply (select "None" to skip)                    |
| `strength_4`     | FLOAT        | Yes      | Strength for fourth LoRA (-10.0 to 10.0, default: 1.0)          |
| `vae_name`       | VAE          | Yes      | VAE model to load                                               |
| `vae_device`     | STRING       | Yes      | Device for VAE ("default" or "cpu") - advanced                  |
| `vae_dtype`      | STRING       | Yes      | Data type for VAE ("bfloat16", "float16", "float32") - advanced |

### Outputs

| Parameter | Type  | Description                                                 |
|-----------|-------|-------------------------------------------------------------|
| `MODEL`   | MODEL | Loaded model with applied LoRAs and optional merge          |
| `CLIP`    | CLIP  | Combined CLIP-L and CLIP-G text encoders with applied LoRAs |
| `VAE`     | VAE   | Loaded VAE                                                  |

### Usage

Extended version of the SDXL loader with support for up to 4 LoRAs and additional VAE configuration options. Load all
model components, optionally merge checkpoints, apply LoRAs sequentially, and configure device/dtype settings for CLIP
and VAE. LoRAs are cached for efficiency.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
