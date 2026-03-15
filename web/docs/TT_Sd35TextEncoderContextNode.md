## TT SD3.5 Text Encoder (Context) *TT_Sd35TextEncoderContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes text prompts for SD3.5 using all three text encoders (CLIP-L, CLIP-G, T5-XXL) from context and returns a configured Guider object.

### Inputs

| Parameter | Type       | Required | Description                                                             |
|-----------|------------|----------|-------------------------------------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object containing model, CLIP, prompts, and resolution settings |

### Outputs

| Parameter | Type       | Description                                             |
|-----------|------------|---------------------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context with guider stored                      |
| `GUIDER`  | GUIDER     | Configured guider with encoded conditioning for sampler |

### Usage

Connect `CONTEXT` from a SD3.5 workflow settings context node. Connect `GUIDER` to a sampler node. Prompts and resolution are read from context — use
`TT SD3.5 GGUF Workflow Settings (Advanced)` to set per-encoder prompts.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
