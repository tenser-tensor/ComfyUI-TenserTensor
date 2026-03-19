## TT FLUX2 Apply ControlNet (Advanced) *TT_Flux2ApplyControlNetAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended version of TT FLUX2 Apply ControlNet with built-in image picker and reference image preview. Supports both connected image input and file
browser selection.

### Inputs

| Parameter             | Type       | Required | Description                                                                                   |
|-----------------------|------------|----------|-----------------------------------------------------------------------------------------------|
| `guider`              | GUIDER     | Yes      | Configured guider from a FLUX2 context or workflow settings node                              |
| `control_net_opt`     | CONTROLNET | No       | Preloaded ControlNet object. If provided, `control_net` combo is ignored                      |
| `reference_image_opt` | IMAGE      | No       | Connected reference image. If provided, `reference_image` file picker is ignored              |
| `vae_opt`             | VAE        | No       | Optional VAE for image preprocessing                                                          |
| `control_net`         | COMBO      | Yes      | ControlNet model file from `models/controlnet`                                                |
| `strength`            | FLOAT      | No       | ControlNet influence strength. Default: `1.0`, range: `0.0` to `10.0`. Set to `0.0` to bypass |
| `start_percent`       | FLOAT      | No       | Step percentage at which ControlNet starts. Default: `0.0`                                    |
| `end_percent`         | FLOAT      | No       | Step percentage at which ControlNet ends. Default: `100.0`                                    |
| `reference_image`     | COMBO      | No       | Reference image file picker with upload support                                               |

### Outputs

| Parameter | Type   | Description                    |
|-----------|--------|--------------------------------|
| `GUIDER`  | GUIDER | Guider with ControlNet applied |

### Usage

Connect `GUIDER` from a FLUX2 workflow settings or context node. Use `reference_image_opt` to pass an image from another node, or use the built-in
file picker to load from disk. Reference image is displayed as a preview after execution. Set `strength=0.0` to bypass ControlNet without
disconnecting the node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
