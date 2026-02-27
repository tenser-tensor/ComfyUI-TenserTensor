## TT Context Set Image *TT_ContextSetImage*

⚠️ Deprecated: This node will be removed in a future major release. Please migrate to the new context nodes.

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Adds or updates image in context object.

### Inputs

| Parameter | Type       | Required | Description               |
|-----------|------------|----------|---------------------------|
| `context` | TT_CONTEXT | Yes      | Context to update         |
| `image`   | IMAGE      | Yes      | Image to store in context |

### Outputs

| Parameter | Type       | Description            |
|-----------|------------|------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context object |

### Usage

Stores pixel-space image in context for use by downstream nodes. Overwrites existing image if present.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
