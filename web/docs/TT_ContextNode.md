## TT Context *TT_ContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

General-purpose context node for FLUX and SDXL workflows. Accepts any combination of pipeline fields and
merges them into the context object. All fields are optional.

### Inputs

| Parameter         | Type               | Required | Description                   |
|-------------------|--------------------|----------|-------------------------------|
| `context`         | TT_CONTEXT         | No       | Existing context to update    |
| `workflow_config` | TT_WORKFLOW_CONFIG | No       | Workflow configuration object |
| `model`           | MODEL              | No       | Diffusion model               |
| `clip`            | CLIP               | No       | CLIP text encoder             |
| `vae`             | VAE                | No       | VAE encoder/decoder           |
| `latent`          | LATENT             | No       | Latent image tensor           |
| `positive`        | CONDITIONING       | No       | Positive conditioning         |
| `negative`        | CONDITIONING       | No       | Negative conditioning         |
| `image`           | IMAGE              | No       | Pixel-space image             |
| `seed`            | INT                | No       | Generation seed               |
| `steps`           | INT                | No       | Number of sampling steps      |
| `cfg`             | FLOAT              | No       | CFG scale                     |

### Outputs

| Parameter         | Type               | Description              |
|-------------------|--------------------|--------------------------|
| `CONTEXT`         | TT_CONTEXT         | Updated context object   |
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Workflow configuration   |
| `MODEL`           | MODEL              | Diffusion model          |
| `CLIP`            | CLIP               | CLIP text encoder        |
| `VAE`             | VAE                | VAE encoder/decoder      |
| `LATENT`          | LATENT             | Latent image tensor      |
| `POSITIVE`        | CONDITIONING       | Positive conditioning    |
| `NEGATIVE`        | CONDITIONING       | Negative conditioning    |
| `IMAGE`           | IMAGE              | Pixel-space image        |
| `SEED`            | INT                | Generation seed          |
| `STEPS`           | INT                | Number of sampling steps |
| `CFG`             | FLOAT              | CFG scale                |

### Usage

Use this node to create or update a context object with any combination of pipeline fields. If `context` is
connected, existing fields are updated with the provided values. If not connected, a new context is created.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
