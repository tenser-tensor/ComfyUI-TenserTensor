## TT FLUX Models Loader (Advanced) *TT_FluxModelsLoaderAdvanced*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended all-in-one model loader for Flux with sampling patches, LoRA support, and advanced settings.

### Inputs

| Parameter             | Type       | Required | Description                                                                       |
|-----------------------|------------|----------|-----------------------------------------------------------------------------------|
| `ckpt_name`           | CHECKPOINT | Yes      | Flux checkpoint to load                                                           |
| `apply_sampling`      | BOOLEAN    | Yes      | Apply sampling shift patch (default: True)                                        |
| `base_sampling_shift` | FLOAT      | Yes      | Base sampling shift value (0.0-100.0, default: 0.5)                               |
| `max_sampling_shift`  | FLOAT      | Yes      | Maximum sampling shift (0.0-100.0, default: 1.15)                                 |
| `sampling_width`      | INT        | Yes      | Width for sampling shift calculation (16-MAX_RESOLUTION, step: 8, default: 1024)  |
| `sampling_height`     | INT        | Yes      | Height for sampling shift calculation (16-MAX_RESOLUTION, step: 8, default: 1024) |
| `clip_l`              | STRING     | Yes      | CLIP-L text encoder model                                                         |
| `t5xxl`               | STRING     | Yes      | T5-XXL text encoder model                                                         |
| `clip_device`         | STRING     | Yes      | Device for CLIP ("default" or "cpu") - advanced                                   |
| `lora_name_1`         | LORA       | Yes      | First LoRA to apply (select "None" to skip)                                       |
| `strength_1`          | FLOAT      | Yes      | Strength for first LoRA (-10.0 to 10.0, default: 1.0)                             |
| `lora_name_2`         | LORA       | Yes      | Second LoRA to apply (select "None" to skip)                                      |
| `strength_2`          | FLOAT      | Yes      | Strength for second LoRA (-10.0 to 10.0, default: 1.0)                            |
| `lora_name_3`         | LORA       | Yes      | Third LoRA to apply (select "None" to skip)                                       |
| `strength_3`          | FLOAT      | Yes      | Strength for third LoRA (-10.0 to 10.0, default: 1.0)                             |
| `lora_name_4`         | LORA       | Yes      | Fourth LoRA to apply (select "None" to skip)                                      |
| `strength_4`          | FLOAT      | Yes      | Strength for fourth LoRA (-10.0 to 10.0, default: 1.0)                            |
| `vae_name`            | VAE        | Yes      | VAE model to load                                                                 |
| `vae_device`          | STRING     | Yes      | Device for VAE ("default" or "cpu") - advanced                                    |
| `vae_dtype`           | STRING     | Yes      | Data type for VAE ("bfloat16", "float16", "float32") - advanced                   |

### Outputs

| Parameter | Type  | Description                                                 |
|-----------|-------|-------------------------------------------------------------|
| `MODEL`   | MODEL | Loaded Flux model with applied patches and LoRAs            |
| `CLIP`    | CLIP  | Combined CLIP-L and T5-XXL text encoders with applied LoRAs |
| `VAE`     | VAE   | Loaded VAE                                                  |

### Usage

Extended Flux loader with optional sampling shift patching for improved high-resolution generation, support for up to 4
LoRAs, and advanced VAE configuration. The sampling shift patch adjusts noise scheduling based on image dimensions.
LoRAs are cached for efficiency.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
