## TT Postproduction (Advanced) *TT_PostproductionAdvanced*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended post-production node with image enhancement, LUT color grading, film grain, and upscaling.

### Inputs

| Parameter             | Type          | Required | Description                                                |
|-----------------------|---------------|----------|------------------------------------------------------------|
| `image`               | IMAGE         | Yes      | Input image to process                                     |
| `image_enhancer`      | BOOLEAN       | Yes      | Enable image enhancement (default: True)                   |
| `brightness_factor`   | FLOAT         | Yes      | Brightness adjustment (-1.0 to 1.0, default: 0.0)          |
| `contrast_factor`     | FLOAT         | Yes      | Contrast multiplier (0.0-5.0, default: 1.0)                |
| `gamma_factor`        | FLOAT         | Yes      | Gamma correction (0.0-3.0, default: 1.0)                   |
| `gamma_gain`          | FLOAT         | Yes      | Gamma gain (0.0-3.0, default: 1.0)                         |
| `hue_factor`          | FLOAT         | Yes      | Hue rotation (-π to π, default: 0.0)                       |
| `saturation_factor`   | FLOAT         | Yes      | Saturation multiplier (0.0-3.0, default: 1.0)              |
| `sharpness_factor`    | FLOAT         | Yes      | Sharpness amount (0.0-3.0, default: 0.0)                   |
| `posterize_bits`      | INT           | Yes      | Posterization bit depth (0-8, default: 8)                  |
| `solarize_thresholds` | FLOAT         | Yes      | Solarization threshold (0.0-1.0, default: 1.0)             |
| `apply_lut`           | BOOLEAN       | Yes      | Enable LUT color grading (default: True)                   |
| `lut_file`            | LUT_FILE      | Yes      | LUT file to apply - advanced                               |
| `lut_strength`        | FLOAT         | Yes      | LUT blend strength (0.0-1.0, default: 1.0)                 |
| `lut_colorspace`      | STRING        | Yes      | Colorspace for LUT (linear/logarithmic) - advanced         |
| `add_film_grain`      | BOOLEAN       | Yes      | Enable film grain effect (default: True)                   |
| `grain_seed`          | INT           | Yes      | Seed for grain pattern (0 to 2^64-1, default: 0)           |
| `grain_scale`         | FLOAT         | Yes      | Grain texture scale (0.25-2.0, default: 0.25)              |
| `grain_strength`      | FLOAT         | Yes      | Grain intensity (0.0-10.0, default: 0.2)                   |
| `grain_saturation`    | FLOAT         | Yes      | Grain color saturation (0.0-2.0, default: 0.5)             |
| `grain_toe`           | FLOAT         | Yes      | Grain distribution toe (-0.2 to 0.5, default: 0.05)        |
| `grain_upscale_mode`  | STRING        | Yes      | Grain interpolation mode - advanced                        |
| `grain_antialias`     | BOOLEAN       | Yes      | Grain antialiasing (default: True)                         |
| `image_upscaler`      | BOOLEAN       | Yes      | Enable image upscaling (default: True)                     |
| `upscaler_device`     | STRING        | Yes      | Device for upscaler (default/cpu) - advanced               |
| `upscale_model_name`  | UPSCALE_MODEL | Yes      | Upscale model to use - advanced                            |
| `upscaler_tile`       | INT           | Yes      | Tile size for upscaling (256-4096, step: 64, default: 512) |
| `upscaler_overlap`    | INT           | Yes      | Tile overlap (0-256, step: 8, default: 64)                 |

### Outputs

| Parameter | Type  | Description                          |
|-----------|-------|--------------------------------------|
| `IMAGE`   | IMAGE | Processed image with applied effects |

### Usage

Complete post-production pipeline with full enhancement controls. Processing order: Image Enhancement → LUT → Film
Grain → Upscale. Toggle each effect on/off independently. Image enhancement includes brightness, contrast, gamma, hue,
saturation, sharpness, posterize, and solarize adjustments. All effects are optional.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
