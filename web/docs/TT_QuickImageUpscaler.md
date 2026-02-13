## TT Quick Image Upscaler *TT_QuickImageUpscaler*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Tiled image upscaler using AI upscale models.

### Inputs

| Parameter            | Type          | Required | Description                                                 |
|----------------------|---------------|----------|-------------------------------------------------------------|
| `image`              | IMAGE         | Yes      | Input image to upscale                                      |
| `device`             | STRING        | Yes      | Device for upscaling (default/cpu) - advanced               |
| `upscale_model_name` | UPSCALE_MODEL | Yes      | Upscale model to use - advanced                             |
| `tile`               | INT           | Yes      | Tile size for processing (256-4096, step: 64, default: 512) |
| `overlap`            | INT           | Yes      | Tile overlap to reduce seams (0-256, step: 8, default: 64)  |

### Outputs

| Parameter | Type  | Description    |
|-----------|-------|----------------|
| `IMAGE`   | IMAGE | Upscaled image |

### Usage

Quick and simple AI upscaling node using tiled processing for memory efficiency. Select an upscale model from your
upscale_models directory. Adjust tile size based on VRAM - smaller tiles use less memory. Increase overlap to reduce
visible seams between tiles.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
