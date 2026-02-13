## TT_KSamplerAdvanced

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Advanced sampler with fine-grained control over denoising steps and noise addition.

### Inputs

| Parameter      | Type         | Required | Description                                               |
|----------------|--------------|----------|-----------------------------------------------------------|
| `model`        | MODEL        | Yes      | The diffusion model to use for sampling                   |
| `positive`     | CONDITIONING | Yes      | Positive conditioning (what to generate)                  |
| `negative`     | CONDITIONING | Yes      | Negative conditioning (what to avoid)                     |
| `latent`       | LATENT       | Yes      | Latent image to denoise                                   |
| `add_noise`    | BOOLEAN      | Yes      | Add noise before sampling (default: True)                 |
| `full_denoise` | BOOLEAN      | Yes      | Complete full denoising (default: False)                  |
| `seed`         | INT          | Yes      | Random seed for reproducibility (0 to 2^64-1, default: 0) |
| `steps`        | INT          | Yes      | Total number of sampling steps (1-10000, default: 25)     |
| `start_step`   | INT          | Yes      | Step to start sampling from (0-10000, default: 0)         |
| `last_step`    | INT          | Yes      | Step to end sampling at (0-10000, default: 10000)         |
| `cfg`          | FLOAT        | Yes      | Classifier-free guidance scale (0.0-100.0, default: 1.5)  |
| `sampler_name` | SAMPLER      | Yes      | Sampler algorithm to use                                  |
| `scheduler`    | SCHEDULER    | Yes      | Noise schedule to use                                     |
| `denoise`      | FLOAT        | Yes      | Denoising strength (0.0-1.0, default: 1.0)                |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `LATENT`  | LATENT | Denoised latent image |

### Usage

Advanced sampler for multi-stage workflows and fine control. Use start_step/last_step for partial denoising, add_noise
to control noise injection, and denoise for strength control. Useful for img2img, refinement passes, and complex
sampling workflows.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
