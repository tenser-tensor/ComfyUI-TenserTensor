## TT SD3.5 GGUF Models Loader (Advanced) *TT_Sd35GgufModelsLoaderAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended GGUF loader for SD3.5 with built-in LoRA support and fine-grained quantization and VAE configuration.

### Inputs

| Parameter         | Type  | Required | Description                                             |
|-------------------|-------|----------|---------------------------------------------------------|
| `diffusion_model` | COMBO | Yes      | GGUF diffusion model file                               |
| `dequant_dtype`   | COMBO | No       | Dequantization dtype, default `bfloat16` (advanced)     |
| `patch_dtype`     | COMBO | No       | Patch dtype, default `bfloat16` (advanced)              |
| `clip_l`          | COMBO | Yes      | CLIP-L text encoder file                                |
| `clip_g`          | COMBO | Yes      | CLIP-G text encoder file                                |
| `t5xxl`           | COMBO | Yes      | T5-XXL text encoder file                                |
| `clip_device`     | COMBO | No       | Device for CLIP inference, default `default` (advanced) |
| `lora_name_1-4`   | COMBO | No       | LoRA files, up to four                                  |
| `strength_1-4`    | FLOAT | No       | LoRA strength, default 1.0, range -10.0 to 10.0         |
| `vae_name`        | COMBO | Yes      | VAE file                                                |
| `vae_device`      | COMBO | No       | Device for VAE inference, default `default` (advanced)  |
| `vae_dtype`       | COMBO | No       | VAE data type (advanced)                                |

### Outputs

| Parameter | Type  | Description            |
|-----------|-------|------------------------|
| `MODEL`   | MODEL | Loaded diffusion model |
| `CLIP`    | CLIP  | Loaded CLIP encoders   |
| `VAE`     | VAE   | Loaded VAE             |

### Usage

Place GGUF diffusion model files in `models/diffusion_models_gguf` or `models/diffusion_models`. Place text encoder files in
`models/text_encoders_gguf`, `models/text_encoders` or `models/clip`. Unused LoRA slots are ignored. Negative LoRA strength values invert the effect.
Adjust `dequant_dtype` and `patch_dtype` if you experience quality or memory issues with the default `bfloat16`.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
