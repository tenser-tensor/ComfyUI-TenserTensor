## TT LTX2.3 GGUF Models Loader *TT_Ltx23GgufModelsLoaderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Loads LTX-Video 2.3 GGUF diffusion model, Gemma 3 12B text encoder, distilled LoRA, and video/audio VAEs in a single node.

### Inputs

| Parameter         | Type  | Required | Description                                                                                    |
|-------------------|-------|----------|------------------------------------------------------------------------------------------------|
| `diffusion_model` | COMBO | Yes      | LTX2.3 GGUF diffusion model file from `models/diffusion_models_gguf`                           |
| `clip`            | COMBO | Yes      | Gemma 3 12B GGUF text encoder file from `models/text_encoders_gguf`                            |
| `distilled_lora`  | COMBO | No       | Distilled LoRA file. Reduces inference steps from 20–40 to ~8 without significant quality loss |
| `strength_model`  | FLOAT | No       | LoRA strength applied to the diffusion model. Default: `1.0`, range: `-2.0` to `2.0`           |
| `strength_clip`   | FLOAT | No       | LoRA strength applied to the text encoder. Default: `1.0`, range: `-2.0` to `2.0`              |
| `video_vae_name`  | COMBO | Yes      | Video VAE file from `models/vae`                                                               |
| `audio_vae_name`  | COMBO | Yes      | Audio VAE file from `models/vae`                                                               |

### Outputs

| Parameter   | Type  | Description                                        |
|-------------|-------|----------------------------------------------------|
| `MODEL`     | MODEL | Loaded diffusion model with distilled LoRA applied |
| `CLIP`      | CLIP  | Loaded Gemma 3 12B text encoder                    |
| `VIDEO_VAE` | VAE   | Video VAE for encoding/decoding video latents      |
| `AUDIO_VAE` | VAE   | Audio VAE for encoding/decoding audio latents      |

### Usage

Use as the entry point for LTX-Video 2.3 pipelines. Connect `MODEL`, `CLIP` to a workflow settings node. Connect `VIDEO_VAE` and `AUDIO_VAE` to a
latent factory node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
