## TT Context Set Image *TT_ContextSetImage*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Adds or updates latent image in context object.

### Inputs

| Parameter | Type       | Required | Description                      |
|-----------|------------|----------|----------------------------------|
| `context` | TT_CONTEXT | Yes      | Context to update                |
| `latent`  | LATENT     | Yes      | Latent image to store in context |

### Outputs

| Parameter | Type       | Description            |
|-----------|------------|------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context object |

### Usage

Stores latent representation in context for use by downstream nodes. Overwrites existing latent if present.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
