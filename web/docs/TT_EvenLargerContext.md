## TT Even Larger Context *TT_EvenLargerContext*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Maximum capacity context node supporting all workflow parameters including ControlNet and masking.

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
| `mask`            | MASK               | No       | Image mask                                                |
| `control_net`     | CONTROL_NET        | No       | ControlNet model                                          |
| `seed`            | INT                | No       | Random seed                                               |
| `steps`           | INT                | No       | Sampling steps                                            |
| `cfg`             | FLOAT              | No       | Classifier-free guidance scale                            |
| `sampler_name`    | COMBO              | No       | Sampler name                                              |
| `scheduler`       | COMBO              | No       | Scheduler name                                            |
| `guidance`        | FLOAT              | No       | Guidance value                                            |
| `clip_l_positive` | STRING             | No       | CLIP-L positive prompt                                    |
| `clip_g_positive` | STRING             | No       | CLIP-G positive prompt                                    |
| `t5xxl_positive`  | STRING             | No       | T5-XXL positive prompt                                    |
| `clip_l_negative` | STRING             | No       | CLIP-L negative prompt                                    |
| `clip_g_negative` | STRING             | No       | CLIP-G negative prompt                                    |
| `t5xxl_negative`  | STRING             | No       | T5-XXL negative prompt                                    |
| `ascore_positive` | FLOAT              | No       | Aesthetic score for positive                              |
| `ascore_negative` | FLOAT              | No       | Aesthetic score for negative                              |
| `width`           | INT                | No       | Image width                                               |
| `height`          | INT                | No       | Image height                                              |
| `target_width`    | INT                | No       | Target width for conditioning                             |
| `target_height`   | INT                | No       | Target height for conditioning                            |

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
| `MASK`            | MASK               | Image mask                  |
| `CONTROL_NET`     | CONTROL_NET        | ControlNet                  |
| `SEED`            | INT                | Random seed                 |
| `STEPS`           | INT                | Sampling steps              |
| `CFG`             | FLOAT              | CFG scale                   |
| `SAMPLER_NAME`    | COMBO              | Sampler name                |
| `SCHEDULER`       | COMBO              | Scheduler name              |
| `GUIDANCE`        | FLOAT              | Guidance value              |
| `CLIP_L_POSITIVE` | STRING             | CLIP-L positive             |
| `CLIP_G_POSITIVE` | STRING             | CLIP-G positive             |
| `T5XXL_POSITIVE`  | STRING             | T5-XXL positive             |
| `CLIP_L_NEGATIVE` | STRING             | CLIP-L negative             |
| `CLIP_G_NEGATIVE` | STRING             | CLIP-G negative             |
| `T5XXL_NEGATIVE`  | STRING             | T5-XXL negative             |
| `ASCORE_POSITIVE` | FLOAT              | Aesthetic score positive    |
| `ASCORE_NEGATIVE` | FLOAT              | Aesthetic score negative    |
| `WIDTH`           | INT                | Width                       |
| `HEIGHT`          | INT                | Height                      |
| `TARGET_WIDTH`    | INT                | Target width                |
| `TARGET_HEIGHT`   | INT                | Target height               |

### Usage

Use this node when you need comprehensive control over all workflow parameters including ControlNet and masking.
Supports both SDXL (CLIP-L/G) and Flux (T5-XXL) conditioning simultaneously.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)