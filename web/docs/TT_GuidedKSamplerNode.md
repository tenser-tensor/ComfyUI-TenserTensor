## TT Guided KSampler *TT_GuidedKSamplerNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Runs guided diffusion sampling using a pre-configured Guider object. Accepts all sampling components as separate inputs for maximum flexibility.

### Inputs

| Parameter      | Type    | Required | Description                         |
|----------------|---------|----------|-------------------------------------|
| `latent`       | LATENT  | Yes      | Input latent tensor                 |
| `guider`       | GUIDER  | Yes      | Configured Guider with conditioning |
| `sigmas`       | SIGMAS  | Yes      | Noise schedule                      |
| `sampler`      | SAMPLER | Yes      | Sampler algorithm                   |
| `random_noise` | NOISE   | Yes      | Noise generator with seed           |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `SAMPLES` | LATENT | Sampled latent tensor |

### Usage

Connect `GUIDER`, `SIGMAS`, and `SAMPLER` outputs from a workflow settings node. `random_noise` comes from a latent factory node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
