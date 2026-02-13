## TT Apply LUT *TT_ApplyLut*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Apply color grading LUT (Look-Up Table) to images for professional color correction.

### Inputs

| Parameter    | Type     | Required | Description                                                    |
|--------------|----------|----------|----------------------------------------------------------------|
| `image`      | IMAGE    | Yes      | Input image to apply LUT to                                    |
| `lut_file`   | LUT_FILE | Yes      | LUT file to apply (from LUT directory) - advanced              |
| `strength`   | FLOAT    | Yes      | Blend strength of LUT effect (0.0-1.0, default: 1.0)           |
| `colorspace` | STRING   | Yes      | Colorspace for LUT application (linear/logarithmic) - advanced |

### Outputs

| Parameter | Type  | Description                          |
|-----------|-------|--------------------------------------|
| `IMAGE`   | IMAGE | Image with applied LUT color grading |

### Usage

Apply professional color grading using LUT files. Place your .cube LUT files in the designated LUT directory. Adjust
strength to blend between original and graded image (1.0 = full LUT, 0.0 = original). Choose colorspace based on your
LUT file's intended working space.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
