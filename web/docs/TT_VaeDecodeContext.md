## TT VAE Decode (Context) *TT_VaeDecodeContext*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Context-based VAE decoder that extracts latent and VAE from context.

### Inputs

| Parameter | Type       | Required | Description                             |
|-----------|------------|----------|-----------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context containing VAE and latent image |

### Outputs

| Parameter | Type       | Description                              |
|-----------|------------|------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context with decoded image added |
| `IMAGE`   | IMAGE      | Decoded image tensor                     |

### Usage

Simplified decoder for context-based workflows. Automatically extracts VAE and latent from context, decodes to image
space, and stores the result back in context. Handles nested tensors and reshapes output to standard format. Raises
error if VAE or latent is missing from context.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
