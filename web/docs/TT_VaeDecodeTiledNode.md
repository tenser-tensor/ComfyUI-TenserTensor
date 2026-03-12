## TT VAE Decode (Tiled) *TT_VaeDecodeTiledNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Decodes a latent tensor to an image using tiled VAE decoding. Useful for large resolutions where full decoding would exceed available VRAM.

### Inputs

| Parameter     | Type   | Required | Description                         |
|---------------|--------|----------|-------------------------------------|
| `vae`         | VAE    | Yes      | VAE model                           |
| `latent`      | LATENT | Yes      | Input latent tensor                 |
| `tile_width`  | INT    | No       | Tile width in pixels, default 512   |
| `tile_height` | INT    | No       | Tile height in pixels, default 512  |
| `overlap`     | INT    | No       | Tile overlap in pixels, default 512 |

### Outputs

| Parameter | Type  | Description   |
|-----------|-------|---------------|
| `IMAGE`   | IMAGE | Decoded image |

### Usage

Increase tile size for better quality at the cost of VRAM. Increase overlap to reduce visible tile seams. Use when decoding high-resolution latents
that cause out-of-memory errors with standard VAE decode.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
