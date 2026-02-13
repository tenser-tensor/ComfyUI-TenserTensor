## TT_ClipTextEncodeSdxl

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

SDXL text encoder with separate CLIP-L and CLIP-G prompt inputs and conditioning parameters.

### Inputs

| Parameter         | Type   | Required | Description                                             |
|-------------------|--------|----------|---------------------------------------------------------|
| `clip`            | CLIP   | Yes      | CLIP text encoder (dual CLIP-L + CLIP-G)                |
| `clip_l_positive` | STRING | Yes      | CLIP-L positive prompt (multiline)                      |
| `clip_g_positive` | STRING | Yes      | CLIP-G positive prompt (multiline)                      |
| `clip_l_negative` | STRING | Yes      | CLIP-L negative prompt (multiline)                      |
| `clip_g_negative` | STRING | Yes      | CLIP-G negative prompt (multiline)                      |
| `ascore_positive` | FLOAT  | Yes      | Aesthetic score for positive (0.0-1000.0, default: 9.0) |
| `ascore_negative` | FLOAT  | Yes      | Aesthetic score for negative (0.0-1000.0, default: 6.0) |
| `width`           | INT    | Yes      | Image width for conditioning (default: 512)             |
| `height`          | INT    | Yes      | Image height for conditioning (default: 512)            |
| `target_width`    | INT    | Yes      | Target width for conditioning (default: 512)            |
| `target_height`   | INT    | Yes      | Target height for conditioning (default: 512)           |

### Outputs

| Parameter  | Type         | Description                                               |
|------------|--------------|-----------------------------------------------------------|
| `POSITIVE` | CONDITIONING | Positive conditioning with aesthetic score and dimensions |
| `NEGATIVE` | CONDITIONING | Negative conditioning with aesthetic score and dimensions |

### Usage

Encode text prompts for SDXL with separate control over CLIP-L and CLIP-G inputs, aesthetic scores, and target
dimensions. The aesthetic scores and dimensions are embedded into the conditioning to guide the generation process.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
