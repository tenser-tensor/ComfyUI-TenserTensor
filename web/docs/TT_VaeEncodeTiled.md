## TT VAE Encode (Tiled) *TT_VaeEncodeTiled*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes large images to latent space using tiled processing to reduce VRAM usage.

### Inputs

| Parameter     | Type  | Required | Description                                         |
|---------------|-------|----------|-----------------------------------------------------|
| `vae`         | VAE   | Yes      | VAE model for encoding                              |
| `image`       | IMAGE | Yes      | Input image to encode                               |
| `tile_width`  | INT   | Yes      | Width of processing tiles in pixels (default: 512)  |
| `tile_height` | INT   | Yes      | Height of processing tiles in pixels (default: 512) |
| `overlap`     | INT   | Yes      | Overlap between tiles in pixels (default: 64)       |

### Outputs

| Parameter | Type   | Description                   |
|-----------|--------|-------------------------------|
| `LATENT`  | LATENT | Encoded latent representation |

### Usage

Processes large images in smaller tiles to reduce memory requirements during VAE encoding. Useful for encoding
high-resolution images that would otherwise cause out-of-memory errors.

Tile size should be set based on available VRAM (smaller tiles = less memory). Overlap prevents visible seams at tile
boundaries - higher overlap produces smoother results but increases processing time. Recommended overlap is 10-15% of
tile size.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
