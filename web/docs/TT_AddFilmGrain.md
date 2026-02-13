## TT Add Film Grain *TT_AddFilmGrain*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Add procedural film grain texture to images for a cinematic look.

### Inputs

| Parameter      | Type    | Required | Description                                                                     |
|----------------|---------|----------|---------------------------------------------------------------------------------|
| `image`        | IMAGE   | Yes      | Input image to add grain to                                                     |
| `seed`         | INT     | Yes      | Random seed for grain pattern (0 to 2^64-1, default: 0)                         |
| `scale`        | FLOAT   | Yes      | Scale of grain texture (0.25-2.0, default: 0.25)                                |
| `strength`     | FLOAT   | Yes      | Intensity of grain effect (0.0-10.0, default: 0.15)                             |
| `saturation`   | FLOAT   | Yes      | Color saturation of grain (0.0-2.0, default: 0.2)                               |
| `toe`          | FLOAT   | Yes      | Toe adjustment for grain distribution (-0.2 to 0.5, default: 0.0)               |
| `upscale_mode` | STRING  | Yes      | Interpolation mode for grain (bilinear/bicubic/lanczos/nearest/area) - advanced |
| `antialias`    | BOOLEAN | Yes      | Enable antialiasing for grain (default: False)                                  |

### Outputs

| Parameter | Type  | Description                   |
|-----------|-------|-------------------------------|
| `IMAGE`   | IMAGE | Image with applied film grain |

### Usage

Add realistic film grain texture to images for a cinematic aesthetic. Adjust scale for grain size, strength for
intensity, and saturation for color. The toe parameter controls the distribution curve of grain in shadows/highlights.
Use different seeds for varied grain patterns.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
