## TT Base Context *TT_BaseContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Creates a new context object from the provided model, clip, vae, and latent inputs. Optionally accepts a
workflow configuration object.

### Inputs

| Parameter         | Type               | Required | Description                   |
|-------------------|--------------------|----------|-------------------------------|
| `model`           | MODEL              | Yes      | Diffusion model               |
| `clip`            | CLIP               | Yes      | CLIP text encoder             |
| `vae`             | VAE                | Yes      | VAE encoder/decoder           |
| `latent`          | LATENT             | Yes      | Latent image tensor           |
| `workflow_config` | TT_WORKFLOW_CONFIG | No       | Workflow configuration object |

### Outputs

| Parameter | Type       | Description                        |
|-----------|------------|------------------------------------|
| `CONTEXT` | TT_CONTEXT | Context object with all fields set |

### Usage

Use this node at the start of a context-driven pipeline to bundle model, clip, vae, and latent into a single
TT_CONTEXT object for use by downstream context nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
