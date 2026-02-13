## TT SDXL Large Context (TT_LargeContextSdxl)

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended context node for SDXL workflows with CLIP-L/G conditioning and aesthetic score inputs.

### Inputs

| Parameter       | Type               | Required | Description                                               |
|-----------------|--------------------|----------|-----------------------------------------------------------|
| context         | TT_CONTEXT         | No       | Existing context to modify (if not provided, creates new) |
| workflow_config | TT_WORKFLOW_CONFIG | No       | Workflow configuration settings                           |
| model           | MODEL              | No       | The diffusion model (UNet/DiT)                            |
| clip            | CLIP               | No       | CLIP text encoder                                         |
| vae             | VAE                | No       | VAE for encoding/decoding                                 |
| positive        | CONDITIONING       | No       | Positive conditioning                                     |
| negative        | CONDITIONING       | No       | Negative conditioning                                     |
| latent          | LATENT             | No       | Latent image tensor                                       |
| image           | IMAGE              | No       | Image tensor                                              |
| seed            | INT                | No       | Random seed                                               |
| steps           | INT                | No       | Sampling steps                                            |
| cfg             | FLOAT              | No       | Classifier-free guidance scale                            |
| sampler_name    | STRING             | No       | Sampler name                                              |
| scheduler       | STRING             | No       | Scheduler name                                            |
| guidance        | FLOAT              | No       | SDXL guidance value                                       |
| clip_l_positive | STRING             | No       | CLIP-L positive prompt                                    |
| clip_g_positive | STRING             | No       | CLIP-G positive prompt                                    |
| clip_l_negative | STRING             | No       | CLIP-L negative prompt                                    |
| clip_g_negative | STRING             | No       | CLIP-G negative prompt                                    |
| ascore_positive | FLOAT              | No       | Aesthetic score for positive                              |
| ascore_negative | FLOAT              | No       | Aesthetic score for negative                              |
| width           | INT                | No       | Image width                                               |
| height          | INT                | No       | Image height                                              |
| target_width    | INT                | No       | Target width for conditioning                             |
| target_height   | INT                | No       | Target height for conditioning                            |

### Outputs

| Parameter       | Type               | Description                 |
|-----------------|--------------------|-----------------------------|
| CONTEXT         | TT_CONTEXT         | Created or modified context |
| WORKFLOW_CONFIG | TT_WORKFLOW_CONFIG | Workflow configuration      |
| MODEL           | MODEL              | Diffusion model             |
| CLIP            | CLIP               | Text encoder                |
| VAE             | VAE                | VAE                         |
| POSITIVE        | CONDITIONING       | Positive conditioning       |
| NEGATIVE        | CONDITIONING       | Negative conditioning       |
| LATENT          | LATENT             | Latent tensor               |
| IMAGE           | IMAGE              | Image tensor                |
| SEED            | INT                | Random seed                 |
| STEPS           | INT                | Sampling steps              |
| CFG             | FLOAT              | CFG scale                   |
| SAMPLER_NAME    | STRING             | Sampler name                |
| SCHEDULER       | STRING             | Scheduler name              |
| GUIDANCE        | FLOAT              | SDXL guidance               |
| CLIP_L_POSITIVE | STRING             | CLIP-L positive             |
| CLIP_G_POSITIVE | STRING             | CLIP-G positive             |
| CLIP_L_NEGATIVE | STRING             | CLIP-L negative             |
| CLIP_G_NEGATIVE | STRING             | CLIP-G negative             |
| ASCORE_POSITIVE | FLOAT              | Aesthetic score positive    |
| ASCORE_NEGATIVE | FLOAT              | Aesthetic score negative    |
| WIDTH           | INT                | Width                       |
| HEIGHT          | INT                | Height                      |
| TARGET_WIDTH    | INT                | Target width                |
| TARGET_HEIGHT   | INT                | Target height               |

### Usage

Use this node for SDXL workflows when you need separate control over CLIP-L and CLIP-G prompts, aesthetic scores, and
target dimensions for conditioning.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)