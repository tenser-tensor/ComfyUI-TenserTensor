## TT Quick Image Upscaler *TT_QuickImageUpscalerNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Upscales an image using a model-based upscaler. All configuration is in advanced inputs — connect an image and run.

### Inputs

| Parameter         | Type  | Required | Description                                   |
|-------------------|-------|----------|-----------------------------------------------|
| `image`           | IMAGE | Yes      | Input image                                   |
| `upscaler_device` | COMBO | No       | Device for upscaling inference (advanced)     |
| `upscale_model`   | COMBO | No       | Upscale model file (advanced)                 |
| `upscale_tile`    | INT   | No       | Tile size in pixels, default 512 (advanced)   |
| `upscale_overlap` | INT   | No       | Tile overlap in pixels, default 64 (advanced) |

### Outputs

| Parameter | Type  | Description    |
|-----------|-------|----------------|
| `IMAGE`   | IMAGE | Upscaled image |

### Usage

Place upscale model files in `models/upscale_models`. Increase tile size for better quality at the cost of VRAM. Increase overlap to reduce visible
tile seams.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
