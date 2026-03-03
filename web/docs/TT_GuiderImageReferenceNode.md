## TT Guider Image Reference *TT_GuiderImageReferenceNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes a reference image into latent space and injects it into a guider's conditioning as reference latents. Useful for image-guided sampling workflows.

### Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `vae` | VAE | Yes | VAE model for encoding the reference image |
| `guider` | GUIDER | Yes | Guider to inject reference latents into |
| `megapixels` | COMBO | Yes | Target resolution for resizing before encoding |
| `resize_method` | COMBO | No | Interpolation method for resizing (advanced) |
| `dimension_step` | INT | No | Align output dimensions to this step size, 1-256 (advanced) |
| `image` | COMBO | Yes | Reference image file to load, with upload support |

### Outputs

| Parameter | Type | Description |
|---|---|---|
| `VAE` | VAE | Passthrough of the input VAE |
| `GUIDER` | GUIDER | Guider with reference latents injected into conditioning |

### Usage

Load a reference image, resize it to the target resolution, encode it with the VAE, and inject the resulting latents into the guider's conditioning. Connect the output `GUIDER` to a sampler to use image-guided sampling.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
