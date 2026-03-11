## TT Canny Edge Detector *TT_CannyEdgeDetectorNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Applies Canny edge detection to a reference image and returns the result as a ControlNet-ready image.

### Inputs

| Parameter         | Type  | Required | Description                                 |
|-------------------|-------|----------|---------------------------------------------|
| `low_threshold`   | FLOAT | Yes      | Lower hysteresis threshold, default 0.4     |
| `high_threshold`  | FLOAT | Yes      | Upper hysteresis threshold, default 0.8     |
| `reference_image` | IMAGE | Yes      | Source image, uploaded directly in the node |

### Outputs

| Parameter | Type  | Description                   |
|-----------|-------|-------------------------------|
| `IMAGE`   | IMAGE | Edge map ready for ControlNet |

### Usage

Connect `IMAGE` output to a ControlNet apply node. The source image is previewed in the node after processing. Increase `high_threshold` for fewer,
stronger edges; decrease `low_threshold` to retain more fine detail.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
