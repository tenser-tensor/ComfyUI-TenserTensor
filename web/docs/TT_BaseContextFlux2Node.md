## TT Base Context FLUX2 *TT_BaseContextFlux2Node*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Creates a new context object for FLUX2 pipelines. Extends the base context with sampler, noise, and sigmas
required for guided diffusion sampling.

### Inputs

| Parameter         | Type               | Required | Description                   |
|-------------------|--------------------|----------|-------------------------------|
| `model`           | MODEL              | Yes      | Diffusion model               |
| `clip`            | CLIP               | Yes      | CLIP text encoder             |
| `vae`             | VAE                | Yes      | VAE encoder/decoder           |
| `latent`          | LATENT             | Yes      | Latent image tensor           |
| `rnd_noise`       | NOISE              | Yes      | Random noise for sampling     |
| `workflow_config` | TT_WORKFLOW_CONFIG | No       | Workflow configuration object |
| `sampler`         | SAMPLER            | No       | Instantiated sampler object   |
| `sigmas`          | SIGMAS             | No       | Sigma schedule for sampling   |

### Outputs

| Parameter | Type       | Description                        |
|-----------|------------|------------------------------------|
| `CONTEXT` | TT_CONTEXT | Context object with all fields set |

### Usage

Use this node at the start of a FLUX2 context-driven pipeline. Bundles all required inputs into a single
TT_CONTEXT object for use by downstream context nodes and guided samplers.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
