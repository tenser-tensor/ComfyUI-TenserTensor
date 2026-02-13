## TT Base Context (TT_BaseContext)

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Creates a foundational context object by combining essential workflow components.

### Inputs

| Parameter         | Type               | Required | Description                     |
|-------------------|--------------------|----------|---------------------------------|
| `model`           | MODEL              | Yes      | The diffusion model (UNet/DiT)  |
| `clip`            | CLIP               | Yes      | CLIP text encoder               |
| `vae`             | VAE                | Yes      | VAE for encoding/decoding       |
| `latent`          | LATENT             | Yes      | Latent image tensor             |
| `workflow_config` | TT_WORKFLOW_CONFIG | No       | Workflow configuration settings |

### Outputs

| Parameter | Type       | Description                                |
|-----------|------------|--------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Dictionary containing all input components |

### Usage

Use this node to package your core workflow components into a single context object that can be passed through your
workflow and modified by other context nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
