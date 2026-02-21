## TT Context Set Guider *TT_ContextSetGuider*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Writes a GUIDER object into the TT_CONTEXT, making it available for downstream context-aware nodes.

### Inputs

| Parameter | Type       | Required | Description                    |
|-----------|------------|----------|--------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object to update       |
| `guider`  | GUIDER     | Yes      | Guider to store in the context |

### Outputs

| Parameter | Type       | Description                                   |
|-----------|------------|-----------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context with `guider` written into it |

### Usage

Sets the `guider` field inside a TT_CONTEXT object. Use this node when you have a guider produced outside the
context pipeline and need to inject it back in for use by subsequent context-aware nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
