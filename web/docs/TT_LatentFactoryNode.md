## TT Latent Factory *TT_LatentFactoryNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Creates a latent tensor and noise for use in sampling pipelines with support for FLUX and SDXL architectures.

### Inputs

| Parameter         | Type  | Required | Description                                                     |
|-------------------|-------|----------|-----------------------------------------------------------------|
| `seed`            | INT   | Yes      | Seed for latent tensor generation                               |
| `noise_seed`      | INT   | Yes      | Seed for noise generation (increments after each run)           |
| `aspect_ratio`    | COMBO | Yes      | Aspect ratio of the latent (1:1, 4:3, 3:2, 16:9, 21:9)          |
| `megapixels`      | COMBO | Yes      | Target resolution in megapixels                                 |
| `orientation`     | COMBO | Yes      | Landscape or portrait orientation                               |
| `model_type`      | COMBO | Yes      | Target model architecture (FLUX1.D, FLUX2.D, SDXL)              |
| `batch_size`      | INT   | No       | Number of latents in batch (1–64, default: 1)                   |
| `clip_multiplier` | COMBO | No       | Multiplier for target CLIP resolution (1x, 2x, 4x, default: 1x) |

### Outputs

| Parameter       | Type   | Description                                   |
|-----------------|--------|-----------------------------------------------|
| `LATENT`        | LATENT | Generated latent tensor                       |
| `RND_NOISE`     | NOISE  | Noise for the sampler                         |
| `SEED`          | INT    | Passthrough of latent seed                    |
| `NOISE_SEED`    | INT    | Passthrough of noise seed                     |
| `MEGAPIXELS`    | STRING | Passthrough of selected megapixels value      |
| `WIDTH`         | INT    | Calculated latent width in pixels             |
| `HEIGHT`        | INT    | Calculated latent height in pixels            |
| `TARGET_WIDTH`  | INT    | CLIP target width (WIDTH × clip_multiplier)   |
| `TARGET_HEIGHT` | INT    | CLIP target height (HEIGHT × clip_multiplier) |

### Usage

Generates a ready-to-use latent and noise pair with reproducible results via independent `seed` and `noise_seed` controls. Dimensions are
automatically calculated from the selected aspect ratio, megapixels, and model architecture. Connect `LATENT` and `RND_NOISE` directly to a sampler,
and pass `TARGET_WIDTH` / `TARGET_HEIGHT` to a CLIP text encoder for conditioning.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
