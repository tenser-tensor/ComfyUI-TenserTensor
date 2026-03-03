## TT Latent MultiTransform On Pixel Space *TT_LatentMultiTransformOnPixelSpaceNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Applies multiple geometric transformations to a latent by first decoding it to pixel space, transforming, and re-encoding. Produces better quality
results than direct latent manipulation.

### Inputs

| Parameter        | Type    | Required | Description                                        |
|------------------|---------|----------|----------------------------------------------------|
| `vae`            | VAE     | Yes      | VAE model for decoding and re-encoding the latent  |
| `latent`         | LATENT  | Yes      | Input latent to transform                          |
| `mask`           | MASK    | No       | Optional noise mask to attach to the output latent |
| `scale_latent`   | BOOLEAN | Yes      | Scale image (Scale) or skip (Skip)                 |
| `scale_factor`   | COMBO   | Yes      | Scale multiplier                                   |
| `scale_method`   | COMBO   | Yes      | Interpolation method for scaling                   |
| `rotate_latent`  | BOOLEAN | Yes      | Rotate image (Rotate) or skip (Skip)               |
| `rotate_angle`   | COMBO   | Yes      | Rotation angle in degrees, clockwise               |
| `flip_latent`    | BOOLEAN | Yes      | Flip image (Flip) or skip (Skip)                   |
| `flip_direction` | COMBO   | Yes      | Flip axis: horizontal or vertical                  |

### Outputs

| Parameter | Type   | Description                       |
|-----------|--------|-----------------------------------|
| `LATENT`  | LATENT | Transformed and re-encoded latent |

### Usage

Decode the latent to pixel space, apply scale, rotation, and flip transformations, then re-encode back to latent space. Transformations are applied in
order: scale → rotate → flip. Requires a VAE — use the same VAE that was used to encode the original latent.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
