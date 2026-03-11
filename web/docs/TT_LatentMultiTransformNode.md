## TT Latent MultiTransform *TT_LatentMultiTransformNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Applies multiple geometric transformations to a latent in a single node: scaling, rotation, and flipping. Each transformation can be enabled or
disabled independently.

### Inputs

| Parameter        | Type    | Required | Description                                            |
|------------------|---------|----------|--------------------------------------------------------|
| `latent`         | LATENT  | Yes      | Input latent to transform                              |
| `mask`           | MASK    | No       | Optional noise mask to attach to the latent            |
| `scale_latent`   | BOOLEAN | Yes      | Scale latent (Scale) or keep original size (Keep size) |
| `scale_factor`   | COMBO   | No       | Scale multiplier (advanced)                            |
| `scale_method`   | COMBO   | No       | Interpolation method for scaling (advanced)            |
| `rotate_latent`  | BOOLEAN | Yes      | Rotate latent (Rotate) or keep orientation (Keep)      |
| `rotate_angle`   | COMBO   | Yes      | Rotation angle in degrees                              |
| `flip_latent`    | BOOLEAN | Yes      | Flip latent (Flip) or keep orientation (Keep)          |
| `flip_direction` | COMBO   | Yes      | Flip axis: horizontal or vertical                      |

### Outputs

| Parameter | Type   | Description        |
|-----------|--------|--------------------|
| `LATENT`  | LATENT | Transformed latent |

### Usage

Apply scale, rotation, and flip to a latent before or after sampling. Transformations are applied in order: scale → rotate → flip. Use the boolean
toggles to enable only the transformations you need.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
