## TT KSampler (Two Stage) *TT_KSamplerTwoStageNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Runs sampling in two sequential stages — draft and refine — in a single node. Draft stage generates a rough result, refine stage continues from where
draft stopped with different sampler settings.

### Inputs

| Parameter              | Type         | Required | Description                                      |
|------------------------|--------------|----------|--------------------------------------------------|
| `model`                | MODEL        | Yes      | Diffusion model                                  |
| `positive`             | CONDITIONING | Yes      | Positive conditioning                            |
| `negative`             | CONDITIONING | Yes      | Negative conditioning                            |
| `latent`               | LATENT       | Yes      | Input latent tensor                              |
| `seed`                 | INT          | Yes      | Generation seed                                  |
| `cfg`                  | FLOAT        | Yes      | Guidance scale, default 3.0                      |
| `draft_steps`          | INT          | Yes      | Number of draft stage steps, default 25          |
| `refiner_steps`        | INT          | Yes      | Number of refine stage steps, default 25         |
| `draft_sampler_name`   | COMBO        | Yes      | Sampler algorithm for draft stage                |
| `draft_scheduler`      | COMBO        | Yes      | Noise schedule for draft stage                   |
| `refiner_sampler_name` | COMBO        | Yes      | Sampler algorithm for refine stage               |
| `refiner_scheduler`    | COMBO        | Yes      | Noise schedule for refine stage                  |
| `draft_denoise`        | FLOAT        | No       | Denoising strength for draft stage, default 1.0  |
| `refiner_denoise`      | FLOAT        | No       | Denoising strength for refine stage, default 1.0 |
| `preview_latent`       | BOOLEAN      | No       | Show step-by-step latent preview during sampling |

### Outputs

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| `LATENT`  | LATENT | Sampled latent tensor |

### Usage

Use different samplers and schedulers for each stage — for example, `dpmpp_2m` with `karras` for draft and `euler` with `normal` for refine. Total
steps equal `draft_steps + refiner_steps`.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
