## TT Image Preview / Save *TT_ImagePreviewSaveNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Previews an image in the node graph and optionally saves it to the output directory.

### Inputs

| Parameter           | Type    | Required | Description                                                    |
|---------------------|---------|----------|----------------------------------------------------------------|
| `image`             | IMAGE   | Yes      | Image to preview and optionally save                           |
| `save_image`        | BOOLEAN | Yes      | Save image to disk (Save image) or preview only (Only preview) |
| `filename_prefix`   | STRING  | Yes      | Prefix for the output filename (default: TT)                   |
| `filename_format`   | COMBO   | No       | Filename format pattern (advanced)                             |
| `subfolder`         | STRING  | No       | Subfolder within the output directory (advanced)               |
| `image_format`      | COMBO   | No       | Output file format: PNG, JPEG, WEBP (advanced)                 |
| `image_quality`     | INT     | No       | JPEG quality, 1-100 (advanced)                                 |
| `compression_level` | INT     | No       | PNG compression level, 0-9 (advanced)                          |

### Outputs

This node has no outputs. It is a terminal output node.

### Usage

Place at the end of a workflow to preview the result and optionally save it to disk. When saving is disabled, the image is still visible in the node
graph as a preview. Use `subfolder` to organize outputs into subdirectories, and `filename_format` to control how files are named.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
