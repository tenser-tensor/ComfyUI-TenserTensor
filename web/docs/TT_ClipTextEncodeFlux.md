## TT_ClipTextEncodeFlux

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Flux text encoder with separate CLIP-L and T5-XXL prompt inputs.

### Inputs

| Parameter         | Type   | Required | Description                                      |
|-------------------|--------|----------|--------------------------------------------------|
| `clip`            | CLIP   | Yes      | CLIP text encoder (dual CLIP-L + T5-XXL)         |
| `clip_l_positive` | STRING | Yes      | CLIP-L positive prompt (multiline)               |
| `t5xxl_positive`  | STRING | Yes      | T5-XXL positive prompt (multiline)               |
| `clip_l_negative` | STRING | Yes      | CLIP-L negative prompt (multiline)               |
| `t5xxl_negative`  | STRING | Yes      | T5-XXL negative prompt (multiline)               |
| `guidance`        | FLOAT  | Yes      | Guidance scale for Flux (1.0-10.0, default: 3.5) |

### Outputs

| Parameter  | Type         | Description                              |
|------------|--------------|------------------------------------------|
| `POSITIVE` | CONDITIONING | Positive conditioning from both encoders |
| `NEGATIVE` | CONDITIONING | Negative conditioning from both encoders |

### Usage

Encode text prompts for Flux with fine-grained control over CLIP-L and T5-XXL inputs separately. Useful when you want
different prompts for each encoder or need precise control over the conditioning process.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
