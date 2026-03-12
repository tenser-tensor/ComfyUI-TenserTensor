## TT VAE Encode (Tiled) *TT_VaeEncodeTiledNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes an image to a latent tensor using tiled VAE encoding. Useful for large resolutions where full encoding would exceed available VRAM.

### Inputs

| Parameter     | Type  | Required | Description                         |
|---------------|-------|----------|-------------------------------------|
| `image`       | IMAGE | Yes      | Input image                         |
| `vae`         | VAE   | Yes      | VAE model                           |
| `tile_width`  | INT   | No       | Tile width in pixels, default 512   |
| `tile_height` | INT   | No       | Tile height in pixels, default 512  |
| `overlap`     | INT   | No       | Tile overlap in pixels, default 512 |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `LATENT`  | LATENT | Encoded latent tensor |

### Usage

Use for img2img or inpainting workflows with high-resolution input images. Increase overlap to reduce visible tile seams at the cost of processing
time.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
