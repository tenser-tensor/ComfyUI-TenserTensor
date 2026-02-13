## TT_VaeDecodeTiled

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Tiled VAE decoder for processing large images without running out of VRAM.

### Inputs

| Parameter     | Type    | Required | Description                                                         |
|---------------|---------|----------|---------------------------------------------------------------------|
| `vae`         | VAE     | Yes      | VAE model for decoding                                              |
| `latent`      | LATENT  | Yes      | Latent image to decode                                              |
| `tile_width`  | INT     | Yes      | Width of each tile in pixels (320-4096, step: 64, default: 512)     |
| `tile_height` | INT     | Yes      | Height of each tile in pixels (320-4096, step: 64, default: 512)    |
| `overlap`     | INT     | Yes      | Overlap between tiles to reduce seams (0-256, step: 8, default: 64) |
| `circular`    | BOOLEAN | Yes      | Enable circular padding for seamless tiling (default: False)        |

### Outputs

| Parameter | Type  | Description          |
|-----------|-------|----------------------|
| `IMAGE`   | IMAGE | Decoded image tensor |

### Usage

Decode large latent images by processing them in smaller tiles. Useful for generating high-resolution images that would
otherwise exceed VRAM capacity. The overlap parameter helps reduce visible seams between tiles. Enable circular padding
for seamless texture generation.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
