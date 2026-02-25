## TT Guider Image Reference *TT_GuiderImageReference*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encode a reference image into latent space and inject it into a Guider's positive conditioning for reference-based generation.

### Inputs

| Parameter        | Type   | Required | Description                                                               |
|------------------|--------|----------|---------------------------------------------------------------------------|
| `vae`            | VAE    | Yes      | VAE model used to encode the reference image                              |
| `guider`         | GUIDER | Yes      | Guider to inject reference latent into                                    |
| `megapixels`     | COMBO  | Yes      | Target resolution for the reference image before encoding                 |
| `upscale_method` | STRING | Yes      | Resampling method for resizing (default: bicubic) - advanced              |
| `dimension_step` | INT    | Yes      | Snaps image dimensions to multiples of this value (default: 1) - advanced |
| `image`          | STRING | Yes      | Reference image from input directory                                      |

### Outputs

| Parameter | Type   | Description                           |
|-----------|--------|---------------------------------------|
| `VAE`     | VAE    | Passthrough VAE for chaining          |
| `GUIDER`  | GUIDER | Guider with reference latent injected |

### Usage

Loads a reference image, resizes it to the target megapixel resolution, encodes it with VAE, and injects the resulting latent into the Guider's
positive conditioning as `reference_latents`. Raises an error if the Guider has no positive conditioning.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
