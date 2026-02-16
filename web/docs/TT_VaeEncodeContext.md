## TT VAE Encode (Context) *TT_VaeEncodeContext*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes pixel image to latent space using VAE from context.

### Inputs

| Parameter | Type       | Required | Description                      |
|-----------|------------|----------|----------------------------------|
| `context` | TT_CONTEXT | Yes      | Context containing VAE and image |

### Outputs

| Parameter | Type       | Description                         |
|-----------|------------|-------------------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context with encoded latent |
| `LATENT`  | LATENT     | Encoded latent representation       |

### Usage

Encodes pixel-space images into latent representations for diffusion processing. Extracts VAE and image from context,
performs encoding, and stores the result back in context.

Requires context to contain both `vae` and `image` components. Raises error if either is missing.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
