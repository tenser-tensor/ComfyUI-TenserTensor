## TT Apply LUT *TT_ApplyLutNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Applies a .cube LUT file to an image for color grading. Supports linear and logarithmic colorspace workflows.

### Inputs

| Parameter    | Type  | Required | Description                                                   |
|--------------|-------|----------|---------------------------------------------------------------|
| `image`      | IMAGE | Yes      | Input image                                                   |
| `lut_file`   | COMBO | Yes      | LUT file from the node pack's `lut/` folder                   |
| `strength`   | FLOAT | No       | Blend strength between original and graded image, default 1.0 |
| `colorspace` | COMBO | No       | Input colorspace — linear or logarithmic                      |

### Outputs

| Parameter | Type  | Description        |
|-----------|-------|--------------------|
| `IMAGE`   | IMAGE | Color graded image |

### Usage

Select a `.cube` LUT file and set colorspace to match your image. Use `strength` below 1.0 to blend the grade with the original. Choose `colorspace`
based on your LUT file's intended working space.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
