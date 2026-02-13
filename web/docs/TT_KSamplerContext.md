## TT KSampler (Context) *TT_KSamplerContext*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Context-based sampler that extracts parameters from workflow context.

### Inputs

| Parameter | Type       | Required | Description                                                         |
|-----------|------------|----------|---------------------------------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context containing model, latent, conditioning, and workflow config |

### Outputs

| Parameter | Type       | Description           |
|-----------|------------|-----------------------|
| `CONTEXT` | TT_CONTEXT | Pass-through context  |
| `LATENT`  | LATENT     | Denoised latent image |

### Usage

Simplified sampler for context-based workflows. Automatically extracts all sampling parameters from the context object:

- Model, positive/negative conditioning, and latent from context
- Seed, steps, cfg, sampler_name, and scheduler from workflow_config

Requires context to contain: model, latent, and workflow_config. Raises error if any required component is missing.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
