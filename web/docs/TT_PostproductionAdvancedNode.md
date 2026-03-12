## TT Postproduction (Advanced) *TT_PostproductionAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

All-in-one postproduction node combining image enhancement, LUT color grading, film grain, and upscaling in a single node. Each stage can be
independently enabled or bypassed.

### Inputs

| Parameter             | Type    | Required | Description                                           |
|-----------------------|---------|----------|-------------------------------------------------------|
| `image`               | IMAGE   | Yes      | Input image                                           |
| `image_enhancer`      | BOOLEAN | No       | Enable image enhancement stage                        |
| `brightness_factor`   | FLOAT   | No       | Brightness adjustment, default 0.0 (neutral)          |
| `contrast_factor`     | FLOAT   | No       | Contrast multiplier, default 1.0 (neutral)            |
| `gamma_factor`        | FLOAT   | No       | Gamma correction, default 1.0 (neutral)               |
| `gamma_gain`          | FLOAT   | No       | Gamma gain, default 1.0 (neutral)                     |
| `hue_factor`          | FLOAT   | No       | Hue rotation in radians, default 0.0 (neutral)        |
| `saturation_factor`   | FLOAT   | No       | Saturation multiplier, default 1.0 (neutral)          |
| `sharpness_factor`    | FLOAT   | No       | Sharpness intensity, default 0.0 (neutral)            |
| `posterize_bits`      | INT     | No       | Color depth in bits, default 8 (neutral)              |
| `solarize_thresholds` | FLOAT   | No       | Solarize threshold, default 1.0 (neutral)             |
| `apply_lut`           | BOOLEAN | No       | Enable LUT color grading stage                        |
| `lut_file`            | COMBO   | No       | LUT file from the node pack's `lut/` folder           |
| `lut_strength`        | FLOAT   | No       | LUT blend strength, default 1.0                       |
| `colorspace`          | COMBO   | No       | Input colorspace — linear or logarithmic              |
| `add_film_grain`      | BOOLEAN | No       | Enable film grain stage                               |
| `grain_seed`          | INT     | No       | Grain generation seed                                 |
| `grain_scale`         | FLOAT   | No       | Grain particle size, default 0.25                     |
| `grain_strength`      | FLOAT   | No       | Grain intensity, default 0.15                         |
| `grain_saturation`    | FLOAT   | No       | Grain color saturation, default 0.2                   |
| `grain_toe`           | FLOAT   | No       | Shadow grain lift, default 0.0                        |
| `grain_upscale_mode`  | COMBO   | No       | Grain interpolation method (advanced)                 |
| `grain_antialias`     | BOOLEAN | No       | Antialiased — smooth grain; Raw — sharp (advanced)    |
| `upscale_image`       | BOOLEAN | No       | Enable upscaling stage                                |
| `upscaler_device`     | COMBO   | No       | Device for upscaling inference (advanced)             |
| `upscale_model`       | COMBO   | No       | Upscale model file (advanced)                         |
| `upscale_tile`        | INT     | No       | Upscale tile size in pixels, default 512 (advanced)   |
| `upscale_overlap`     | INT     | No       | Upscale tile overlap in pixels, default 64 (advanced) |

### Outputs

| Parameter | Type  | Description          |
|-----------|-------|----------------------|
| `IMAGE`   | IMAGE | Post-processed image |

### Usage

Stages run in order: enhancement → LUT → grain → upscale. Bypass any stage with its toggle. All enhancement parameters default to neutral values —
only active adjustments are applied.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)