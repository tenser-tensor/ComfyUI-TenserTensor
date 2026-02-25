## TT Latent Factory *TT_LatentFactory*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Generates empty latent images with precise dimension control based on aspect ratio and megapixel count.
Automatically calculates correct dimensions for FLUX and SDXL models, plus separate CLIP conditioning sizes.

### Inputs

| Parameter         | Type   | Required | Description                                                   |
|-------------------|--------|----------|---------------------------------------------------------------|
| `seed`            | INT    | Yes      | Seed for reproducible results (0 – 18446744073709551615)      |
| `noise_seed`      | INT    | Yes      | Separate seed for noise generation (0 – 18446744073709551615) |
| `aspect_ratio`    | STRING | Yes      | Image proportions (1:1, 4:3, 3:2, 16:9, 21:9)                 |
| `megapixels`      | COMBO | Yes      | Total resolution (0.25 MP, 0.5 MP, 1 MP, 2 MP, 4 MP, 8 MP)    |
| `orientation`     | STRING | Yes      | Image orientation (landscape / portrait)                      |
| `model_type`      | STRING | Yes      | Target model architecture (FLUX1.D, FLUX2.D, SDXL)            |
| `batch_size`      | INT    | Yes      | Number of latents to generate (1–64, default: 1) - advanced   |
| `clip_multiplier` | STRING | Yes      | CLIP target size multiplier (1x, 2x, 4x) - advanced           |

### Outputs

| Parameter       | Type   | Description                              |
|-----------------|--------|------------------------------------------|
| `LATENT`        | LATENT | Empty latent tensor ready for sampling   |
| `RANDOM_NOISE`  | NOISE  | Noise object seeded with `noise_seed`    |
| `SEED`          | INT    | Generation seed                          |
| `NOISE_SEED`    | INT    | Noise seed                               |
| `MEGAPIXELS`    | COMBO  | Selected megapixel value for chaining    |
| `WIDTH`         | INT    | Calculated image width (multiple of 64)  |
| `HEIGHT`        | INT    | Calculated image height (multiple of 64) |
| `TARGET_WIDTH`  | INT    | CLIP conditioning target width           |
| `TARGET_HEIGHT` | INT    | CLIP conditioning target height          |

### Usage

Select aspect ratio, resolution, and orientation to automatically compute pixel dimensions suited for the chosen
model. FLUX1.D uses 16-channel latents, FLUX2.D uses 128-channel, SDXL uses 4-channel. `clip_multiplier` scales the TARGET
dimensions relative to the image dimensions — useful for multi-resolution CLIP conditioning. Connect `RANDOM_NOISE`
directly to a sampler node for reproducible noise tied to `noise_seed`.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
