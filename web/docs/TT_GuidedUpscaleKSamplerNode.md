## TT Guided Upscale KSampler *TT_GuidedUpscaleKSamplerNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Runs guided diffusion sampling with optional latent upscaling after generation. Extends the standard Guided KSampler with a built-in upscale step.

### Inputs

| Parameter      | Type    | Required | Description                                        |
|----------------|---------|----------|----------------------------------------------------|
| `latent`       | LATENT  | Yes      | Input latent tensor                                |
| `guider`       | GUIDER  | Yes      | Configured Guider with conditioning                |
| `sigmas`       | SIGMAS  | Yes      | Noise schedule                                     |
| `sampler`      | SAMPLER | Yes      | Sampler algorithm                                  |
| `random_noise` | NOISE   | Yes      | Noise generator with seed                          |
| `scale_latent` | BOOLEAN | Yes      | Enable latent upscaling after sampling             |
| `scale_factor` | COMBO   | No       | Upscale multiplier, default `1x` (advanced)        |
| `scale_method` | COMBO   | No       | Interpolation method, default `bicubic` (advanced) |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `SAMPLES` | LATENT | Sampled latent tensor |

### Usage

Toggle `scale_latent` to enable upscaling after sampling. Scale factor and method are in advanced inputs. Use for hi-res fix workflows without a
separate upscale node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
