## TT CLIP Text Encode SDXL (Context) *TT_ClipTextEncodeSdxlContext*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Context-based SDXL text encoder that extracts prompts and parameters from workflow config.

### Inputs

| Parameter | Type       | Required | Description                                                                     |
|-----------|------------|----------|---------------------------------------------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context containing CLIP encoder and workflow config with prompts and parameters |

### Outputs

| Parameter  | Type         | Description                                               |
|------------|--------------|-----------------------------------------------------------|
| `CONTEXT`  | TT_CONTEXT   | Updated context with positive/negative conditioning added |
| `POSITIVE` | CONDITIONING | Positive conditioning with aesthetic score and dimensions |
| `NEGATIVE` | CONDITIONING | Negative conditioning with aesthetic score and dimensions |

### Usage

Simplified encoder for context-based SDXL workflows. Automatically extracts all encoding parameters from
workflow_config:

- `clip_l_positive`, `clip_g_positive` for positive prompts
- `clip_l_negative`, `clip_g_negative` for negative prompts
- `ascore_positive`, `ascore_negative` for aesthetic scores
- `width`, `height`, `target_width`, `target_height` for dimensions

Updates context with the generated conditioning and also returns them separately for convenient access.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
