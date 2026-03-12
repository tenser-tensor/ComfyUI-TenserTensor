## TT Image Enhancer *TT_ImageEnhancerNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Applies a range of image enhancement operations in a single node. Each parameter has a neutral default — only active adjustments are applied.

### Inputs

| Parameter             | Type  | Required | Description                                                |
|-----------------------|-------|----------|------------------------------------------------------------|
| `image`               | IMAGE | Yes      | Input image                                                |
| `brightness_factor`   | FLOAT | No       | Brightness adjustment, default 0.0 (neutral)               |
| `contrast_factor`     | FLOAT | No       | Contrast multiplier, default 1.0 (neutral)                 |
| `gamma_factor`        | FLOAT | No       | Gamma correction, default 1.0 (neutral)                    |
| `gamma_gain`          | FLOAT | No       | Gamma gain, default 1.0 (neutral)                          |
| `hue_factor`          | FLOAT | No       | Hue rotation in radians, default 0.0 (neutral)             |
| `saturation_factor`   | FLOAT | No       | Saturation multiplier, default 1.0 (neutral)               |
| `sharpness_factor`    | FLOAT | No       | Sharpness intensity, default 0.0 (neutral)                 |
| `posterize_bits`      | INT   | No       | Color depth in bits, default 8 (neutral, no posterization) |
| `solarize_thresholds` | FLOAT | No       | Solarize threshold, default 1.0 (neutral, no solarization) |

### Outputs

| Parameter | Type  | Description    |
|-----------|-------|----------------|
| `IMAGE`   | IMAGE | Enhanced image |

### Usage

All parameters default to neutral values — adjustments are only applied when values differ from defaults. Powered by Kornia.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
