## TT FLUX2 Apply ControlNet *TT_Flux2ApplyControlNetNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Applies a ControlNet to a FLUX2 guider using a reference image. Supports preloaded ControlNet objects and optional VAE for image preprocessing.

### Inputs

| Parameter         | Type       | Required | Description                                                                                   |
|-------------------|------------|----------|-----------------------------------------------------------------------------------------------|
| `guider`          | GUIDER     | Yes      | Configured guider from a FLUX2 context or workflow settings node                              |
| `reference_image` | IMAGE      | Yes      | Reference image for ControlNet conditioning                                                   |
| `control_net_opt` | CONTROLNET | No       | Preloaded ControlNet object. If provided, `control_net` combo is ignored                      |
| `vae_opt`         | VAE        | No       | Optional VAE for image preprocessing                                                          |
| `control_net`     | COMBO      | Yes      | ControlNet model file from `models/controlnet`                                                |
| `strength`        | FLOAT      | No       | ControlNet influence strength. Default: `1.0`, range: `0.0` to `10.0`. Set to `0.0` to bypass |
| `start_percent`   | FLOAT      | No       | Step percentage at which ControlNet starts. Default: `0.0`                                    |
| `end_percent`     | FLOAT      | No       | Step percentage at which ControlNet ends. Default: `100.0`                                    |

### Outputs

| Parameter | Type   | Description                    |
|-----------|--------|--------------------------------|
| `GUIDER`  | GUIDER | Guider with ControlNet applied |

### Usage

Connect `GUIDER` from a FLUX2 workflow settings or context node. Connect output `GUIDER` to a guided sampler node. Set `strength=0.0` to bypass
ControlNet without disconnecting the node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
