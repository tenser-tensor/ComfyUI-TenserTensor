## TT Context Extract Guided Sampler (FLUX2) *TT_ContextExtractGuidedSamplerFlux2Node*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extracts latent, guider, sigmas, sampler, and noise from a context object for use with a FLUX2 guided sampler node.

### Inputs

| Parameter | Type       | Required | Description                                  |
|-----------|------------|----------|----------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object from an upstream context node |

### Outputs

| Parameter   | Type       | Description                         |
|-------------|------------|-------------------------------------|
| `CONTEXT`   | TT_CONTEXT | Context passthrough                 |
| `LATENT`    | LATENT     | Latent tensor                       |
| `GUIDER`    | GUIDER     | Configured guider with conditioning |
| `SIGMAS`    | SIGMAS     | Noise schedule                      |
| `SAMPLER`   | SAMPLER    | Sampler algorithm                   |
| `RND_NOISE` | NOISE      | Noise generator with seed           |

### Usage

Connect `CONTEXT` from a FLUX2 context node. Connect outputs directly to a guided sampler node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
