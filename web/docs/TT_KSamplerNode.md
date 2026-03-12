## TT KSampler *TT_KSamplerNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Standard KSampler node with built-in latent preview support. Accepts model, conditioning, and latent as separate inputs.

### Inputs

| Parameter        | Type         | Required | Description                                      |
|------------------|--------------|----------|--------------------------------------------------|
| `model`          | MODEL        | Yes      | Diffusion model                                  |
| `positive`       | CONDITIONING | Yes      | Positive conditioning                            |
| `negative`       | CONDITIONING | Yes      | Negative conditioning                            |
| `latent`         | LATENT       | Yes      | Input latent tensor                              |
| `seed`           | INT          | Yes      | Generation seed                                  |
| `steps`          | INT          | Yes      | Number of sampling steps, default 30             |
| `cfg`            | FLOAT        | Yes      | Guidance scale, default 3.0                      |
| `sampler_name`   | COMBO        | Yes      | Sampler algorithm                                |
| `scheduler`      | COMBO        | Yes      | Noise schedule                                   |
| `preview_latent` | BOOLEAN      | No       | Show step-by-step latent preview during sampling |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `LATENT`  | LATENT | Sampled latent tensor |

### Usage

Connect `MODEL`, `CONDITIONING`, and `LATENT` outputs from loader and encoder nodes. Enable `preview_latent` to see intermediate results during
sampling.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
