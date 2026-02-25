## TT Image Preview / Upscale / Save *TT_ImagePreviewUpscaleSave*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Combined preview, upscale, and save node with flexible output options.

### Inputs

| Parameter            | Type    | Required | Description                                                                                                                               |
|----------------------|---------|----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `image`              | IMAGE   | Yes      | Input image tensor to preview, upscale, or save                                                                                           |
| `save_image`         | BOOLEAN | Yes      | Enable/disable saving to disk (default: Enabled)                                                                                          |
| `filename_prefix`    | STRING  | Yes      | Prefix for output filename (default: "tenser-tensor")                                                                                     |
| `filename_format`    | STRING  | Yes      | Naming pattern: "name-###" (prefix-00001), "date-name-###" (2026-02-16-prefix-00001), "name-datetime" (prefix-20260216-143045) - advanced |
| `subfolder`          | STRING  | Yes      | Optional subfolder within output directory (empty = root output folder) - advanced                                                        |
| `image_format`       | STRING  | Yes      | Output format: PNG, JPEG, or WEBP (default: PNG) - advanced                                                                               |
| `image_quality`      | INT     | Yes      | Quality for JPEG and WEBP formats (0-100, default: 100). Ignored for PNG - advanced                                                       |
| `compression_level`  | INT     | Yes      | Compression level for PNG format (0-9, default: 9). Ignored for JPEG and WEBP - advanced                                                  |
| `upscale_image`      | BOOLEAN | Yes      | Enable/disable upscaling (default: Enabled)                                                                                               |
| `upscaler_device`    | STRING  | Yes      | Device for upscaling: "default" or "cpu" - advanced                                                                                       |
| `upscale_model_name` | STRING  | Yes      | Upscale model selected from available upscale_models - advanced                                                                           |
| `tile`               | INT     | Yes      | Tile size for tiled upscaling (256-4096, step 64, default: 512) - advanced                                                                |
| `overlap`            | INT     | Yes      | Overlap between tiles in pixels (0-256, step 8, default: 64) - advanced                                                                   |

### Outputs

This is an output node with no return values. Images are displayed in the UI and optionally upscaled and saved to disk.

### Usage

All-in-one node that can preview, upscale, and save images in a single step. Upscaling is applied before saving — the upscaled result is both displayed in the UI and written to disk. When `upscale_image` is disabled, the original image is used. When `save_image` is disabled, the image is only previewed in the UI without writing to disk.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
