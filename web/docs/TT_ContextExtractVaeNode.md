## TT Context Extract VAE *TT_ContextExtractVaeNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extracts the VAE from the context for direct connection to a VAE encoder or decoder node.

### Inputs

| Parameter | Type       | Required | Description    |
|-----------|------------|----------|----------------|
| `context` | TT_CONTEXT | Yes      | Context object |

### Outputs

| Parameter | Type       | Description                |
|-----------|------------|----------------------------|
| `CONTEXT` | TT_CONTEXT | Passthrough context object |
| `VAE`     | VAE        | VAE encoder/decoder        |

### Usage

Use this node to extract the VAE from the context and connect it directly to a VAE encoder or decoder node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
