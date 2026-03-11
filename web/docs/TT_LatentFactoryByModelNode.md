## TT Latent Factory (By Model) *TT_LatentFactoryByModelNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Creates an empty latent tensor with dimensions and channel count automatically derived from the connected model. Supports any model architecture
without manual configuration.

### Inputs

| Parameter         | Type  | Required | Description                                                   |
|-------------------|-------|----------|---------------------------------------------------------------|
| `model`           | MODEL | Yes      | Diffusion model — latent format is read from it automatically |
| `seed`            | INT   | Yes      | Generation seed                                               |
| `noise_seed`      | INT   | Yes      | Noise seed, randomized after each generation                  |
| `aspect_ratio`    | COMBO | Yes      | Aspect ratio of the output image                              |
| `megapixels`      | COMBO | Yes      | Target resolution in megapixels                               |
| `orientation`     | COMBO | Yes      | Landscape or portrait                                         |
| `batch_size`      | INT   | No       | Number of latents per batch, default 1 (advanced)             |
| `clip_multiplier` | COMBO | No       | Multiplier for CLIP target dimensions, default 1x (advanced)  |

### Outputs

| Parameter       | Type   | Description                                   |
|-----------------|--------|-----------------------------------------------|
| `MODEL`         | MODEL  | Passthrough model for chaining nodes          |
| `LATENT`        | LATENT | Empty latent tensor                           |
| `RND_NOISE`     | NOISE  | Noise generator configured with noise seed    |
| `SEED`          | INT    | Generation seed                               |
| `NOISE_SEED`    | INT    | Noise seed                                    |
| `MEGAPIXELS`    | STRING | Selected megapixel value                      |
| `WIDTH`         | INT    | Calculated image width in pixels              |
| `HEIGHT`        | INT    | Calculated image height in pixels             |
| `TARGET_WIDTH`  | INT    | CLIP target width (width × clip_multiplier)   |
| `TARGET_HEIGHT` | INT    | CLIP target height (height × clip_multiplier) |

### Usage

Connect any diffusion model — the node reads latent channel count and spatial downscale ratio directly from it. Use `MODEL` passthrough output to
continue the node chain without an extra connection.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
