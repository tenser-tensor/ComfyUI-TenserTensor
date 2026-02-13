## TT Postproduction *TT_Postproduction*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

All-in-one post-production node combining LUT color grading, film grain, and upscaling.

### Inputs

| Parameter            | Type          | Required | Description                                                |
|----------------------|---------------|----------|------------------------------------------------------------|
| `image`              | IMAGE         | Yes      | Input image to process                                     |
| `apply_lut`          | BOOLEAN       | Yes      | Enable LUT color grading (default: True)                   |
| `lut_file`           | LUT_FILE      | Yes      | LUT file to apply - advanced                               |
| `lut_strength`       | FLOAT         | Yes      | LUT blend strength (0.0-1.0, default: 1.0)                 |
| `lut_colorspace`     | STRING        | Yes      | Colorspace for LUT (linear/logarithmic) - advanced         |
| `add_film_grain`     | BOOLEAN       | Yes      | Enable film grain effect (default: True)                   |
| `grain_seed`         | INT           | Yes      | Seed for grain pattern (0 to 2^64-1, default: 0)           |
| `grain_scale`        | FLOAT         | Yes      | Grain texture scale (0.25-2.0, default: 0.25)              |
| `grain_strength`     | FLOAT         | Yes      | Grain intensity (0.0-10.0, default: 0.2)                   |
| `grain_saturation`   | FLOAT         | Yes      | Grain color saturation (0.0-2.0, default: 0.5)             |
| `grain_toe`          | FLOAT         | Yes      | Grain distribution toe (-0.2 to 0.5, default: 0.05)        |
| `grain_upscale_mode` | STRING        | Yes      | Grain interpolation mode - advanced                        |
| `grain_antialias`    | BOOLEAN       | Yes      | Grain antialiasing (default: True)                         |
| `image_upscaler`     | BOOLEAN       | Yes      | Enable image upscaling (default: True)                     |
| `upscaler_device`    | STRING        | Yes      | Device for upscaler (default/cpu) - advanced               |
| `upscale_model_name` | UPSCALE_MODEL | Yes      | Upscale model to use - advanced                            |
| `upscaler_tile`      | INT           | Yes      | Tile size for upscaling (256-4096, step: 64, default: 512) |
| `upscaler_overlap`   | INT           | Yes      | Tile overlap (0-256, step: 8, default: 64)                 |

### Outputs

| Parameter | Type  | Description                          |
|-----------|-------|--------------------------------------|
| `IMAGE`   | IMAGE | Processed image with applied effects |

### Usage

Complete post-production pipeline in one node. Toggle each effect on/off with boolean switches. Processing order: LUT →
Film Grain → Upscale. Disable any effect by setting its toggle to False. All effects are optional and can be used
independently or combined.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
