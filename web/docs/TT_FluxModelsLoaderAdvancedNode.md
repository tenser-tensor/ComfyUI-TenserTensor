## TT FLUX Models Loader (Advanced) *TT_FluxModelsLoaderAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended FLUX pipeline loader with sampling shift control, up to 4 LoRA slots, and advanced device/dtype configuration.

### Inputs

| Parameter           | Type    | Required | Description                                                                                      |
|---------------------|---------|----------|--------------------------------------------------------------------------------------------------|
| `diffusion_model`   | COMBO   | Yes      | FLUX diffusion model checkpoint file                                                             |
| `apply_sampling`    | BOOLEAN | Yes      | Enable resolution-based sampling shift ("Flux Shift" / "No Shift", default: enabled)            |
| `base_sampling_shift` | FLOAT | Yes      | Base shift value for sampling schedule (0.0–100.0, default: 0.5) *(advanced)*                   |
| `max_sampling_shift`  | FLOAT | Yes      | Maximum shift value for sampling schedule (0.0–100.0, default: 1.15) *(advanced)*               |
| `sampling_width`    | INT     | Yes      | Reference width for shift calculation (16–MAX, step: 8, default: 1024) *(advanced)*             |
| `sampling_height`   | INT     | Yes      | Reference height for shift calculation (16–MAX, step: 8, default: 1024) *(advanced)*            |
| `clip_l`            | COMBO   | Yes      | CLIP-L text encoder file                                                                         |
| `t5xxl`             | COMBO   | Yes      | T5-XXL text encoder file                                                                         |
| `clip_device`       | COMBO   | Yes      | Device for CLIP/T5 inference (default: "default") *(advanced)*                                  |
| `lora_name_1`       | COMBO   | Yes      | LoRA file for slot 1                                                                             |
| `strength_1`        | FLOAT   | Yes      | Strength for LoRA slot 1 (-10.0–10.0, default: 1.0)                                             |
| `lora_name_2`       | COMBO   | Yes      | LoRA file for slot 2                                                                             |
| `strength_2`        | FLOAT   | Yes      | Strength for LoRA slot 2 (-10.0–10.0, default: 1.0)                                             |
| `lora_name_3`       | COMBO   | Yes      | LoRA file for slot 3                                                                             |
| `strength_3`        | FLOAT   | Yes      | Strength for LoRA slot 3 (-10.0–10.0, default: 1.0)                                             |
| `lora_name_4`       | COMBO   | Yes      | LoRA file for slot 4                                                                             |
| `strength_4`        | FLOAT   | Yes      | Strength for LoRA slot 4 (-10.0–10.0, default: 1.0)                                             |
| `vae_name`          | COMBO   | Yes      | VAE model file for image encoding/decoding                                                       |
| `vae_device`        | COMBO   | Yes      | Device for VAE inference (default: "default") *(advanced)*                                      |
| `vae_dtype`         | COMBO   | Yes      | Data type for VAE computation *(advanced)*                                                       |

### Outputs

| Parameter | Type  | Description                      |
|-----------|-------|----------------------------------|
| `MODEL`   | MODEL | Loaded FLUX diffusion model      |
| `CLIP`    | CLIP  | Loaded CLIP+T5 text encoder      |
| `VAE`     | VAE   | Loaded VAE                       |

### Usage

Advanced version of the FLUX pipeline loader with full control over all loading parameters. Supports up to
4 simultaneous LoRAs applied at load time. Enable "Flux Shift" to apply resolution-aware sampling shift —
adjust `base_sampling_shift`, `max_sampling_shift`, and the reference resolution to tune the shift curve.
Use advanced device/dtype options to offload components to specific devices or reduce memory usage.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
