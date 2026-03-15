## TT LTX2.3 Text Encoder (Context) *TT_Ltx23TextEncoderContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes text prompts for LTX-Video 2.3 using Gemma 3 12B from context and returns a configured Guider object ready for sampling.

### Inputs

| Parameter | Type       | Required | Description                                                    |
|-----------|------------|----------|----------------------------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object containing model, CLIP, prompts, and frame rate |

### Outputs

| Parameter | Type       | Description                                             |
|-----------|------------|---------------------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context with guider stored                      |
| `GUIDER`  | GUIDER     | Configured guider with encoded conditioning for sampler |

### Usage

Connect `CONTEXT` from a LTX2.3 workflow settings context node. Connect `GUIDER` to a sampler node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
