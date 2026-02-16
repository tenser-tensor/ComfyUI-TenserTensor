## TT Image Preview / Save *TT_ImagePreviewSave*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Combined preview and save node with flexible output options.

### Inputs

| Parameter           | Type    | Required | Description                                                                                                                               |
|---------------------|---------|----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `image`             | IMAGE   | Yes      | Input image tensor to preview or save                                                                                                     |
| `save_image`        | BOOLEAN | Yes      | Enable/disable saving to disk (default: Enabled)                                                                                          |
| `filename_prefix`   | STRING  | Yes      | Prefix for output filename (default: "tenser-tensor")                                                                                     |
| `filename_format`   | STRING  | Yes      | Naming pattern: "name-###" (prefix-00001), "date-name-###" (2026-02-16-prefix-00001), "name-datetime" (prefix-20260216-143045) - advanced |
| `subfolder`         | STRING  | Yes      | Optional subfolder within output directory (empty = root output folder) - advanced                                                        |
| `image_format`      | STRING  | Yes      | Output format: PNG, JPEG, or WEBP (default: PNG) - advanced                                                                               |
| `image_quality`     | INT     | Yes      | Quality for JPEG and WEBP formats (0-100, default: 100). Ignored for PNG                                                                  |
| `compression_level` | INT     | Yes      | Compression level for PNG format (0-9, default: 9). Ignored for JPEG and WEBP                                                             |

### Outputs

This is an output node with no return values. Images are displayed in the UI and optionally saved to disk.

### Usage

Dual-purpose node that can preview images in the UI and/or save them to disk with extensive formatting options.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
