## TT Context *TT_ContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

General-purpose context node for FLUX and SDXL workflows. Merges or updates fields in an existing context object. All fields are optional.

### Inputs

| Parameter         | Type               | Required | Description                       |
|-------------------|--------------------|----------|-----------------------------------|
| `context`         | TT_CONTEXT         | No       | Existing context object to update |
| `workflow_config` | TT_WORKFLOW_CONFIG | No       | Workflow configuration object     |
| `model`           | MODEL              | No       | Diffusion model                   |
| `clip`            | CLIP               | No       | CLIP text encoder                 |
| `vae`             | VAE                | No       | VAE encoder/decoder               |
| `latent`          | LATENT             | No       | Latent tensor                     |
| `positive`        | CONDITIONING       | No       | Positive conditioning             |
| `negative`        | CONDITIONING       | No       | Negative conditioning             |
| `image`           | IMAGE              | No       | Image tensor                      |
| `seed`            | INT                | No       | Sampling seed                     |
| `steps`           | INT                | No       | Number of denoising steps         |
| `cfg`             | FLOAT              | No       | Classifier-free guidance scale    |

### Outputs

| Parameter         | Type               | Description                       |
|-------------------|--------------------|-----------------------------------|
| `CONTEXT`         | TT_CONTEXT         | Updated context object            |
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Workflow config passthrough       |
| `MODEL`           | MODEL              | Model passthrough                 |
| `CLIP`            | CLIP               | CLIP passthrough                  |
| `VAE`             | VAE                | VAE passthrough                   |
| `LATENT`          | LATENT             | Latent passthrough                |
| `POSITIVE`        | CONDITIONING       | Positive conditioning passthrough |
| `NEGATIVE`        | CONDITIONING       | Negative conditioning passthrough |
| `IMAGE`           | IMAGE              | Image passthrough                 |
| `SEED`            | INT                | Seed passthrough                  |
| `STEPS`           | INT                | Steps passthrough                 |
| `CFG`             | FLOAT              | CFG passthrough                   |

### Usage

Use to update or extend an existing context object mid-pipeline. Connect `context` from an upstream context node and override only the fields you
need.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
