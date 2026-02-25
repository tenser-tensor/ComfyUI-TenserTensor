## TT FLUX2 GGUF Models Loader *TT_GgufModelsLoader*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Load GGUF-quantized diffusion model (UNet), CLIP text encoder, and VAE in a single node.

### Inputs

| Parameter   | Type   | Required | Description                        |
|-------------|--------|----------|------------------------------------|
| `unet_name` | STRING | Yes      | GGUF UNet/diffusion model filename |
| `clip_name` | STRING | Yes      | GGUF CLIP text encoder filename    |
| `vae_name`  | STRING | Yes      | VAE model filename                 |

### Outputs

| Parameter | Type  | Description            |
|-----------|-------|------------------------|
| `MODEL`   | MODEL | Loaded diffusion model |
| `CLIP`    | CLIP  | Loaded text encoder    |
| `VAE`     | VAE   | Loaded VAE decoder     |

### Usage

All-in-one loader for GGUF-quantized FLUX2 models. Place your `.gguf` diffusion model files in the `diffusion_models` or `unet` directory, CLIP files in
`text_encoders` or `clip` directory. VAE can be any standard ComfyUI-compatible VAE file.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
