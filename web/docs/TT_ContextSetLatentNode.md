## TT Context Set Latent *TT_ContextSetLatentNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Sets the latent field in an existing context object.

### Inputs

| Parameter | Type       | Required | Description              |
|-----------|------------|----------|--------------------------|
| `context` | TT_CONTEXT | Yes      | Context object to update |
| `latent`  | LATENT     | Yes      | Latent image tensor      |

### Outputs

| Parameter | Type       | Description            |
|-----------|------------|------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context object |

### Usage

Use this node to update the latent in the context after sampling or encoding.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
