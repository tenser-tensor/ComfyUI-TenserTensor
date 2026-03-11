## TT Guided KSampler (With Preview) *TT_GuidedKSamplerWithPreviewNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Runs guided diffusion sampling with optional step-by-step latent preview in the ComfyUI interface. Identical to TT Guided KSampler with an added
preview toggle.

### Inputs

| Parameter        | Type    | Required | Description                                |
|------------------|---------|----------|--------------------------------------------|
| `latent`         | LATENT  | Yes      | Input latent tensor                        |
| `guider`         | GUIDER  | Yes      | Configured Guider with conditioning        |
| `sigmas`         | SIGMAS  | Yes      | Noise schedule                             |
| `sampler`        | SAMPLER | Yes      | Sampler algorithm                          |
| `random_noise`   | NOISE   | Yes      | Noise generator with seed                  |
| `preview_latent` | BOOLEAN | Yes      | Show intermediate previews during sampling |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `SAMPLES` | LATENT | Sampled latent tensor |

### Usage

Enable `preview_latent` to display latent previews at each sampling step in the node interface. Note: ComfyUI launches with previews disabled by
default — this node overrides that setting automatically.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
