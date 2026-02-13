## TT Image Enhancer *TT_ImageEnhancer*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Comprehensive image adjustment node with multiple enhancement controls.

### Inputs

| Parameter             | Type  | Required | Description                                                              |
|-----------------------|-------|----------|--------------------------------------------------------------------------|
| `image`               | IMAGE | Yes      | Input image to enhance                                                   |
| `brightness_factor`   | FLOAT | Yes      | Brightness adjustment (-1.0 to 1.0, default: 0.0, 0.0=no effect)         |
| `contrast_factor`     | FLOAT | Yes      | Contrast multiplier (0.0-5.0, default: 1.0, 1.0=no effect)               |
| `gamma_factor`        | FLOAT | Yes      | Gamma correction value (0.0-3.0, default: 1.0, 1.0=no effect)            |
| `gamma_gain`          | FLOAT | Yes      | Gamma gain multiplier (0.0-3.0, default: 1.0, 1.0=no effect)             |
| `hue_factor`          | FLOAT | Yes      | Hue rotation in radians (-π to π, default: 0.0, 0.0=no effect)           |
| `saturation_factor`   | FLOAT | Yes      | Saturation multiplier (0.0-3.0, default: 1.0, 1.0=no effect)             |
| `sharpness_factor`    | FLOAT | Yes      | Sharpness amount (0.0-3.0, default: 0.0, 0.0=no effect)                  |
| `posterize_bits`      | INT   | Yes      | Bit depth for posterization (0-8, default: 8, 8=no effect)               |
| `solarize_thresholds` | FLOAT | Yes      | Threshold for solarization effect (0.0-1.0, default: 1.0, 1.0=no effect) |

### Outputs

| Parameter | Type  | Description                             |
|-----------|-------|-----------------------------------------|
| `IMAGE`   | IMAGE | Enhanced image with applied adjustments |

### Usage

All-in-one image enhancement node for adjusting brightness, contrast, colors, and applying effects. Use default values (
brightness: 0.0, contrast/gamma/saturation: 1.0, posterize: 8, solarize: 1.0) for no effect. Adjust individual
parameters as needed - effects are applied sequentially.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
