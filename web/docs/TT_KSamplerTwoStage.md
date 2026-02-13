## TT KSampler (Two Stages) *TT_KSamplerTwoStage*

Two-stage sampler with separate draft and refinement passes.

### Inputs

| Parameter              | Type         | Required | Description                                                |
|------------------------|--------------|----------|------------------------------------------------------------|
| `model`                | MODEL        | Yes      | The diffusion model to use for sampling                    |
| `positive`             | CONDITIONING | Yes      | Positive conditioning (what to generate)                   |
| `negative`             | CONDITIONING | Yes      | Negative conditioning (what to avoid)                      |
| `latent`               | LATENT       | Yes      | Latent image to denoise                                    |
| `seed`                 | INT          | Yes      | Random seed for reproducibility (0 to 2^64-1, default: 0)  |
| `cfg`                  | FLOAT        | Yes      | Classifier-free guidance scale (0.0-100.0, default: 1.5)   |
| `draft_steps`          | INT          | Yes      | Number of steps for draft pass (1-10000, default: 25)      |
| `refiner_steps`        | INT          | Yes      | Number of steps for refinement pass (1-10000, default: 25) |
| `draft_sampler_name`   | COMBO        | Yes      | Sampler algorithm for draft pass                           |
| `draft_scheduler`      | COMBO        | Yes      | Noise schedule for draft pass                              |
| `refiner_sampler_name` | COMBO        | Yes      | Sampler algorithm for refinement pass                      |
| `refiner_scheduler`    | COMBO        | Yes      | Noise schedule for refinement pass                         |
| `draft_denoise`        | FLOAT        | Yes      | Denoising strength for draft (0.0-1.0, default: 0.7)       |
| `refiner_denoise`      | FLOAT        | Yes      | Denoising strength for refinement (0.0-1.0, default: 1.0)  |

### Outputs

| Parameter | Type   | Description                             |
|-----------|--------|-----------------------------------------|
| `LATENT`  | LATENT | Fully denoised latent after both passes |

### Usage

Automated two-stage sampling workflow. First performs a draft pass with partial denoising, then refines the result with
a second pass. Each stage can use different samplers, schedulers, and step counts. Useful for quick previews followed by
quality refinement, or combining different sampling strategies.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
