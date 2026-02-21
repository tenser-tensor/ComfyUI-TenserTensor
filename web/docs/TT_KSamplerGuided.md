## TT KSampler (Guided) *TT_KSamplerGuided*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Guided latent sampler that takes a pre-configured guider, sigmas, sampler, and noise to produce denoised latent samples.

### Inputs

| Parameter      | Type    | Required | Description                             |
|----------------|---------|----------|-----------------------------------------|
| `latent`       | LATENT  | Yes      | Input latent to sample from             |
| `guider`       | GUIDER  | Yes      | Configured guider with encoded prompt   |
| `sigmas`       | SIGMAS  | Yes      | Sigma schedule for the sampling process |
| `sampler`      | SAMPLER | Yes      | Instantiated sampler object             |
| `random_noise` | NOISE   | Yes      | Noise source for the diffusion process  |

### Outputs

| Parameter | Type   | Description             |
|-----------|--------|-------------------------|
| `SAMPLES` | LATENT | Denoised latent samples |

### Usage

Runs guided diffusion sampling on the input latent. Connect a guider from a text encoder node, sigmas from a
scheduler, and a sampler from a workflow settings node. `random_noise` controls stochasticity — use a seeded
noise node for reproducible results.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
