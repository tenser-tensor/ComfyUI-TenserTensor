# TT Latent Factory

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Generate empty latent images with precise dimension control based on aspect ratio and megapixel count.

Automatically calculates correct dimensions for FLUX and SDXL models, plus separate CLIP conditioning sizes.

## Parameters

| Parameter         | Type     | Description                                       |
|-------------------|----------|---------------------------------------------------|
| `aspect_ratio`    | DROPDOWN | Image proportions (1:1, 4:3, 3:2, 16:9, 21:9)     |
| `megapixels`      | DROPDOWN | Total resolution (0.5 MP, 1 MP, 2 MP, 4 MP, 8 MP) |
| `orientation`     | DROPDOWN | landscape or portrait                             |
| `model_type`      | DROPDOWN | FLUX (16 channels) or SDXL (4 channels)           |
| `clip_multiplier` | DROPDOWN | CLIP target size multiplier (1x, 2x, 4x)          |
| `batch_size`      | INT      | Number of latents to generate (default: 1)        |

## Outputs

| Output        | Type   | Description                                         |
|---------------|--------|-----------------------------------------------------|
| `latent`      | LATENT | Empty latent image tensor with random noise         |
| `width`       | INT    | Calculated image width (rounded to multiple of 64)  |
| `height`      | INT    | Calculated image height (rounded to multiple of 64) |
| `clip_width`  | INT    | CLIP conditioning target width                      |
| `clip_height` | INT    | CLIP conditioning target height                     |

## Example

Select 16:9, 2 MP, landscape, FLUX, 2x → generates 1920×1088 latent with 3840×2176 CLIP dimensions.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
