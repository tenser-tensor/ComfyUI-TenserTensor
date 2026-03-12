## TT VAE Decode (Context) *TT_VaeDecodeContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Decodes a latent tensor to an image using VAE, reading all required data from a connected context object.

### Inputs

| Parameter | Type    | Required | Description                                 |
|-----------|---------|----------|---------------------------------------------|
| `context` | CONTEXT | Yes      | Pipeline context with VAE and latent tensor |

### Outputs

| Parameter | Type    | Description                      |
|-----------|---------|----------------------------------|
| `CONTEXT` | CONTEXT | Passthrough context for chaining |
| `IMAGE`   | IMAGE   | Decoded image                    |

### Usage

Connect a context output from a sampler node. VAE and latent are read from the context automatically. Use in context-driven pipelines to keep node
connections minimal.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
