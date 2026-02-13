## TT KSampler *TT_KSampler*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Standard sampler node for generating images from latents.

### Inputs

| Parameter      | Type         | Required | Description                                               |
|----------------|--------------|----------|-----------------------------------------------------------|
| `model`        | MODEL        | Yes      | The diffusion model to use for sampling                   |
| `positive`     | CONDITIONING | Yes      | Positive conditioning (what to generate)                  |
| `negative`     | CONDITIONING | Yes      | Negative conditioning (what to avoid)                     |
| `latent`       | LATENT       | Yes      | Latent image to denoise                                   |
| `seed`         | INT          | Yes      | Random seed for reproducibility (0 to 2^64-1, default: 0) |
| `steps`        | INT          | Yes      | Number of sampling steps (1-10000, default: 25)           |
| `cfg`          | FLOAT        | Yes      | Classifier-free guidance scale (0.0-100.0, default: 1.5)  |
| `sampler_name` | SAMPLER      | Yes      | Sampler algorithm to use                                  |
| `scheduler`    | SCHEDULER    | Yes      | Noise schedule to use                                     |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `LATENT`  | LATENT | Denoised latent image |

### Usage

Standard KSampler for generating images. Accepts all common sampling parameters and returns a denoised latent ready for
VAE decoding.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
