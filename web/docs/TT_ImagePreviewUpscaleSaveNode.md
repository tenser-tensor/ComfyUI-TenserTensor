## TT Image Preview / Upscale / Save *TT_ImagePreviewUpscaleSaveNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Previews an image in the node graph with optional upscaling via a dedicated upscale model and optional saving to the output directory.

### Inputs

| Parameter           | Type    | Required | Description                                                                   |
|---------------------|---------|----------|-------------------------------------------------------------------------------|
| `image`             | IMAGE   | Yes      | Image to preview, upscale, and optionally save                                |
| `save_image`        | BOOLEAN | Yes      | Save image to disk (Save image) or preview only (Only preview)                |
| `upscale_image`     | BOOLEAN | Yes      | Upscale image before saving (Upscale image) or keep original size (Keep size) |
| `filename_prefix`   | STRING  | Yes      | Prefix for the output filename (default: TT)                                  |
| `filename_format`   | COMBO   | No       | Filename format pattern (advanced)                                            |
| `subfolder`         | STRING  | No       | Subfolder within the output directory (advanced)                              |
| `image_format`      | COMBO   | No       | Output file format: PNG, JPEG, WEBP (advanced)                                |
| `image_quality`     | INT     | No       | JPEG quality, 1-100 (advanced)                                                |
| `compression_level` | INT     | No       | PNG compression level, 0-9 (advanced)                                         |
| `upscaler_device`   | COMBO   | No       | Device to run the upscale model on (advanced)                                 |
| `upscale_model`     | COMBO   | No       | Upscale model to use (advanced)                                               |
| `upscale_tile`      | INT     | No       | Tile size for tiled upscaling, 128-4096 (advanced)                            |
| `upscale_overlap`   | INT     | No       | Overlap between tiles in pixels, 8-256 (advanced)                             |

### Outputs

This node has no outputs. It is a terminal output node.

### Usage

Place at the end of a workflow to upscale, preview, and optionally save the result. When upscaling is enabled, the image is processed through the
selected upscale model before saving. Tiled upscaling is used to handle large images with limited VRAM — reduce `upscale_tile` if you run into
out-of-memory errors.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
