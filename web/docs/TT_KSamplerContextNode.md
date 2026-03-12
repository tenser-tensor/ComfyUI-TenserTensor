## TT KSampler (Context) *TT_KSamplerContextNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Context-based KSampler that reads all sampling parameters from a connected context object. Designed for use in context-driven pipelines where model,
latent, and workflow config are passed as a single object.

### Inputs

| Parameter        | Type    | Required | Description                                              |
|------------------|---------|----------|----------------------------------------------------------|
| `context`        | CONTEXT | Yes      | Pipeline context with model, latent, and workflow config |
| `preview_latent` | BOOLEAN | No       | Show step-by-step latent preview during sampling         |

### Outputs

| Parameter | Type    | Description                         |
|-----------|---------|-------------------------------------|
| `CONTEXT` | CONTEXT | Updated context with sampled latent |
| `LATENT`  | LATENT  | Sampled latent tensor               |

### Usage

Connect a context output from a workflow settings or text encoder node. The node reads `model`, `latent`, `seed`, `steps`, `cfg`, `sampler_name`, and
`scheduler` from the context automatically. Sampled latent is written back into the context for downstream nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
