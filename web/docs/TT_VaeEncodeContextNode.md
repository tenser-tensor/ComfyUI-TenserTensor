## TT VAE Encode (Context) *TT_VaeEncodeContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes an image to a latent tensor using VAE, reading all required data from a connected context object.

### Inputs

| Parameter | Type    | Required | Description                               |
|-----------|---------|----------|-------------------------------------------|
| `context` | CONTEXT | Yes      | Pipeline context with VAE and pixel image |

### Outputs

| Parameter | Type    | Description                      |
|-----------|---------|----------------------------------|
| `CONTEXT` | CONTEXT | Passthrough context for chaining |
| `LATENT`  | LATENT  | Encoded latent tensor            |

### Usage

Connect a context output from an image loader or upstream node. VAE and image are read from the context automatically. Use in context-driven pipelines
for img2img or inpainting workflows.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
