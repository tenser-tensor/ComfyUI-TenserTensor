## TT Add Film Grain *TT_AddFilmGrainNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Adds procedural film grain to an image. Grain is generated from a seed for reproducibility and can be tuned for scale, intensity, color, and shadow detail.

### Inputs

| Parameter      | Type    | Required | Description                                              |
|----------------|---------|----------|----------------------------------------------------------|
| `image`        | IMAGE   | Yes      | Input image                                              |
| `seed`         | INT     | Yes      | Grain generation seed                                    |
| `scale`        | FLOAT   | No       | Grain particle size, default 0.25                        |
| `strength`     | FLOAT   | No       | Grain intensity, default 0.15                            |
| `saturation`   | FLOAT   | No       | Grain color saturation, default 0.2                      |
| `toe`          | FLOAT   | No       | Shadow grain lift, default 0.0                           |
| `upscale_mode` | COMBO   | No       | Interpolation method for grain upscaling (advanced)      |
| `antialias`    | BOOLEAN | No       | Antialiased — smooth grain edges; Raw — sharp (advanced) |

### Outputs

| Parameter | Type  | Description          |
|-----------|-------|----------------------|
| `IMAGE`   | IMAGE | Image with film grain|

### Usage

Lower `scale` for fine grain, higher for coarse. Increase `saturation` for colored grain typical of film stocks. Use `toe` to add grain in shadow areas only.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
