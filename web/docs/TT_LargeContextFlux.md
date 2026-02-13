## TT FLUX Large Context (TT_LargeContextFlux)

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended context node for Flux workflows with additional CLIP and T5 conditioning inputs.

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
| `sampler_name`    | STRING             | No       | Sampler name                                              |
| `scheduler`       | STRING             | No       | Scheduler name                                            |
| `guidance`        | FLOAT              | No       | Flux guidance value                                       |
| `clip_l_positive` | STRING             | No       | CLIP-L positive prompt                                    |
| `t5xxl_positive`  | STRING             | No       | T5-XXL positive prompt                                    |
| `clip_l_negative` | STRING             | No       | CLIP-L negative prompt                                    |
| `t5xxl_negative`  | STRING             | No       | T5-XXL negative prompt                                    |
| `width`           | INT                | No       | Image width                                               |
| `height`          | INT                | No       | Image height                                              |

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
| `SAMPLER_NAME`    | STRING             | Sampler name                |
| `SCHEDULER`       | STRING             | Scheduler name              |
| `GUIDANCE`        | FLOAT              | Flux guidance               |
| `CLIP_L_POSITIVE` | STRING             | CLIP-L positive             |
| `T5XXL_POSITIVE`  | STRING             | T5-XXL positive             |
| `CLIP_L_NEGATIVE` | STRING             | CLIP-L negative             |
| `T5XXL_NEGATIVE`  | STRING             | T5-XXL negative             |
| `WIDTH`           | INT                | Width                       |
| `HEIGHT`          | INT                | Height                      |

### Usage

Use this node for Flux workflows when you need fine-grained control over CLIP-L and T5-XXL prompts separately, along
with Flux-specific guidance settings.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)