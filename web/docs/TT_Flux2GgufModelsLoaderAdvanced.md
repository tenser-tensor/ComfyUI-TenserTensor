## TT FLUX2 GGUF Models Loader (Advanced) *TT_GgufModelsLoaderAdvanced*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

All-in-one loader for GGUF-quantized models with extended control over quantization, sampling, and LoRA support.

### Inputs

| Parameter             | Type    | Required | Advanced | Description                                                            |
|-----------------------|---------|----------|----------|------------------------------------------------------------------------|
| `unet_name`           | STRING  | Yes      |          | GGUF UNet/diffusion model filename                                     |
| `dequant_dtype`       | STRING  | Yes      | Yes      | Data type for dequantization (default/target/float32/float16/bfloat16) |
| `patch_dtype`         | STRING  | Yes      | Yes      | Data type for weight patching                                          |
| `apply_sampling`      | BOOLEAN | Yes      |          | Enable/disable flux sampling shift patch                               |
| `base_sampling_shift` | FLOAT   | Yes      | Yes      | Base shift value for flux sampling (default: 0.5)                      |
| `max_sampling_shift`  | FLOAT   | Yes      | Yes      | Maximum shift value for flux sampling (default: 1.15)                  |
| `sampling_width`      | INT     | Yes      | Yes      | Reference width for sampling shift calculation                         |
| `sampling_height`     | INT     | Yes      | Yes      | Reference height for sampling shift calculation                        |
| `lora_name_1..4`      | STRING  | Yes      | Yes      | LoRA filename (None to skip)                                           |
| `strength_1..4`       | FLOAT   | Yes      | Yes      | LoRA blend strength (-10.0 to 10.0, default: 1.0)                      |
| `clip_name`           | STRING  | Yes      |          | GGUF CLIP text encoder filename                                        |
| `vae_name`            | STRING  | Yes      |          | VAE model filename                                                     |
| `vae_device`          | STRING  | Yes      | Yes      | Device for VAE (default/cpu)                                           |
| `vae_dtype`           | STRING  | Yes      | Yes      | Data type for VAE (bfloat16/float16/float32)                           |

### Outputs

| Parameter | Type  | Description            |
|-----------|-------|------------------------|
| `MODEL`   | MODEL | Loaded diffusion model |
| `CLIP`    | CLIP  | Loaded text encoder    |
| `VAE`     | VAE   | Loaded VAE decoder     |

### Usage

Extended version of FLUX2 GGUF Models Loader. Supports up to 4 LoRAs loaded simultaneously. Enable `apply_sampling` to apply flux sampling shift patch —
useful for improving quality at non-standard resolutions. Advanced parameters are hidden by default and can be revealed via the node's show/hide
controls.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
