## TT KSampler (Advanced) *TT_KSamplerAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended KSampler with fine-grained control over noise, denoising range, and step boundaries. Useful for multi-stage workflows and img2img.

### Inputs

| Parameter        | Type         | Required | Description                                             |
|------------------|--------------|----------|---------------------------------------------------------|
| `model`          | MODEL        | Yes      | Diffusion model                                         |
| `positive`       | CONDITIONING | Yes      | Positive conditioning                                   |
| `negative`       | CONDITIONING | Yes      | Negative conditioning                                   |
| `latent`         | LATENT       | Yes      | Input latent tensor                                     |
| `add_noise`      | BOOLEAN      | Yes      | Random Noise — use random noise; Zero Noise — use zeros |
| `full_denoise`   | BOOLEAN      | Yes      | Complete — force full denoise; Partial — stop early     |
| `denoise`        | FLOAT        | Yes      | Denoising strength, default 1.0                         |
| `seed`           | INT          | Yes      | Generation seed                                         |
| `steps`          | INT          | Yes      | Total number of sampling steps, default 30              |
| `cfg`            | FLOAT        | Yes      | Guidance scale, default 3.0                             |
| `start_step`     | INT          | No       | Step to start sampling from, default 0                  |
| `last_step`      | INT          | No       | Step to stop sampling at, default 10000                 |
| `sampler_name`   | COMBO        | Yes      | Sampler algorithm                                       |
| `scheduler`      | COMBO        | Yes      | Noise schedule                                          |
| `preview_latent` | BOOLEAN      | No       | Show step-by-step latent preview during sampling        |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `LATENT`  | LATENT | Sampled latent tensor |

### Usage

Use `start_step` and `last_step` to run only a portion of the schedule — useful for chaining two samplers in a draft/refine workflow. Set `add_noise`
to Zero Noise when passing a pre-noised latent from a previous stage.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
