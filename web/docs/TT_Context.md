## TT Context *TT_Context*

⚠️ Deprecated: This node will be removed in a future major release. Please migrate to the new context nodes.

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Standard context node that can create a new context or modify an existing one.

### Inputs

| Parameter         | Type               | Required | Description                                               |
|-------------------|--------------------|----------|-----------------------------------------------------------|
| `context`         | TT_CONTEXT         | No       | Existing context to modify (if not provided, creates new) |
| `workflow_config` | TT_WORKFLOW_CONFIG | No       | Workflow configuration settings                           |
| `model`           | MODEL              | No       | The diffusion model (UNet/DiT)                            |
| `clip`            | CLIP               | No       | CLIP text encoder                                         |
| `vae`             | VAE                | No       | VAE for encoding/decoding                                 |
| `positive`        | CONDITIONING       | No       | Positive conditioning                                     |
| `negative`        | CONDITIONING       | No       | Negative conditioning                                     |
| `latent`          | LATENT             | No       | Latent image tensor                                       |
| `image`           | IMAGE              | No       | Image tensor                                              |
| `seed`            | INT                | No       | Random seed                                               |
| `steps`           | INT                | No       | Sampling steps                                            |
| `cfg`             | FLOAT              | No       | Classifier-free guidance scale                            |
| `sampler_name`    | COMBO              | No       | Sampler name                                              |
| `scheduler`       | COMBO              | No       | Scheduler name                                            |

### Outputs

| Parameter         | Type               | Description                 |
|-------------------|--------------------|-----------------------------|
| `CONTEXT`         | TT_CONTEXT         | Created or modified context |
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Workflow configuration      |
| `MODEL`           | MODEL              | Diffusion model             |
| `CLIP`            | CLIP               | Text encoder                |
| `VAE`             | VAE                | VAE                         |
| `POSITIVE`        | CONDITIONING       | Positive conditioning       |
| `NEGATIVE`        | CONDITIONING       | Negative conditioning       |
| `LATENT`          | LATENT             | Latent tensor               |
| `IMAGE`           | IMAGE              | Image tensor                |
| `SEED`            | INT                | Random seed                 |
| `STEPS`           | INT                | Sampling steps              |
| `CFG`             | FLOAT              | CFG scale                   |
| `SAMPLER_NAME`    | COMBO              | Sampler name                |
| `SCHEDULER`       | COMBO              | Scheduler name              |

### Usage

Use this node to create a new context from scratch or modify specific parameters in an existing context. All parameters
are optional - provide only what you need to set or change.


---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
