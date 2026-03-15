## TT LTX2.3 GGUF Models Loader (Advanced) *TT_Ltx23GgufModelsLoaderAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended version of TT LTX2.3 GGUF Models Loader with support for up to 4 additional LoRAs, GGUF dequantization options, and per-device/dtype control for VAEs.

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `diffusion_model` | COMBO | Yes | LTX2.3 GGUF diffusion model file from `models/diffusion_models_gguf` |
| `dequant_dtype` | COMBO | No | dtype used for GGUF dequantization. Default: `bfloat16` |
| `patch_dtype` | COMBO | No | dtype used for patching GGUF layers. Default: `bfloat16` |
| `clip` | COMBO | Yes | Gemma 3 12B GGUF text encoder file from `models/text_encoders_gguf` |
| `clip_device` | COMBO | No | Device for text encoder inference. Default: `default` |
| `lora_name_1` – `lora_name_4` | COMBO | No | Additional LoRA files from `models/loras` |
| `strength_1` – `strength_4` | FLOAT | No | Strength for each additional LoRA. Default: `1.0`, range: `-10.0` to `10.0` |
| `distilled_lora` | COMBO | No | Distilled LoRA file. Reduces inference steps from 20–40 to ~8 |
| `strength_model` | FLOAT | No | Distilled LoRA strength applied to the diffusion model. Default: `1.0`, range: `-2.0` to `2.0` |
| `strength_clip` | FLOAT | No | Distilled LoRA strength applied to the text encoder. Default: `1.0`, range: `-2.0` to `2.0` |
| `video_vae_name` | COMBO | Yes | Video VAE file from `models/vae` |
| `video_vae_device` | COMBO | No | Device for video VAE inference. Default: `default` |
| `video_vae_dtype` | COMBO | No | dtype for video VAE. Default: `bfloat16` |
| `audio_vae_name` | COMBO | Yes | Audio VAE file from `models/vae` |

### Outputs

| Parameter | Type | Description |
|-----------|------|-------------|
| `MODEL` | MODEL | Loaded diffusion model with LoRAs applied |
| `CLIP` | CLIP | Loaded Gemma 3 12B text encoder |
| `VIDEO_VAE` | VAE | Video VAE for encoding/decoding video latents |
| `AUDIO_VAE` | VAE | Audio VAE for encoding/decoding audio latents |

### Usage

Use when you need fine-grained control over model loading. Connect `MODEL`, `CLIP` to a workflow settings node. Connect `VIDEO_VAE` and `AUDIO_VAE` to a latent factory node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)