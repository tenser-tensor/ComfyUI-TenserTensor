## TT_ClipTextEncodeFluxContext

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Context-based Flux text encoder that extracts prompts from workflow config.

### Inputs

| Parameter | Type       | Required | Description                                                      |
|-----------|------------|----------|------------------------------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context containing CLIP encoder and workflow config with prompts |

### Outputs

| Parameter  | Type         | Description                                               |
|------------|--------------|-----------------------------------------------------------|
| `CONTEXT`  | TT_CONTEXT   | Updated context with positive/negative conditioning added |
| `POSITIVE` | CONDITIONING | Positive conditioning from both encoders                  |
| `NEGATIVE` | CONDITIONING | Negative conditioning from both encoders                  |

### Usage

Simplified encoder for context-based workflows. Automatically extracts CLIP-L and T5-XXL prompts plus guidance from
workflow_config:

- `clip_l_positive`, `t5xxl_positive` for positive prompts
- `clip_l_negative`, `t5xxl_negative` for negative prompts
- `guidance` for Flux guidance scale

Updates context with the generated conditioning and also returns them separately for convenient access.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
