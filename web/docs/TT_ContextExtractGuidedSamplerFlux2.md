## TT Context Extract Guided Sampler FLUX2 *TT_ContextExtractGuidedSamplerFlux2*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extracts latent, guider, sigmas, sampler, and noise from the context for direct connection to a FLUX2 guided
sampler node.

### Inputs

| Parameter | Type       | Required | Description    |
|-----------|------------|----------|----------------|
| `context` | TT_CONTEXT | Yes      | Context object |

### Outputs

| Parameter  | Type       | Description                    |
|------------|------------|--------------------------------|
| `CONTEXT`  | TT_CONTEXT | Passthrough context object     |
| `LATENT`   | LATENT     | Latent image tensor            |
| `GUIDER`   | GUIDER     | Guider object for sampling     |
| `SIGMAS`   | SIGMAS     | Sigma schedule for sampling    |
| `SAMPLER`  | SAMPLER    | Instantiated sampler object    |
| `RND_NOISE`| NOISE      | Random noise for sampling      |

### Usage

Use this node to extract all inputs required by a guided sampler from the context, avoiding manual wire
routing for each parameter.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
