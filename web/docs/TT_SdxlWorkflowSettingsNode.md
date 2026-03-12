## TT SDXL Workflow Settings *TT_SdxlWorkflowSettingsNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Configures global workflow parameters for SDXL pipelines. Outputs a workflow config object alongside individual parameters for direct node
connections.

### Inputs

| Parameter         | Type  | Required | Description                                            |
|-------------------|-------|----------|--------------------------------------------------------|
| `seed`            | INT   | Yes      | Generation seed                                        |
| `steps`           | INT   | Yes      | Number of sampling steps, default 30                   |
| `cfg`             | FLOAT | Yes      | Guidance scale, default 5.0                            |
| `sampler_name`    | COMBO | Yes      | Sampler algorithm                                      |
| `scheduler`       | COMBO | Yes      | Noise schedule                                         |
| `ascore_positive` | FLOAT | Yes      | Aesthetic score for positive conditioning, default 9.0 |
| `ascore_negative` | FLOAT | Yes      | Aesthetic score for negative conditioning, default 6.0 |
| `width`           | INT   | Yes      | Image width in pixels                                  |
| `height`          | INT   | Yes      | Image height in pixels                                 |
| `target_width`    | INT   | No       | CLIP target width (advanced)                           |
| `target_height`   | INT   | No       | CLIP target height (advanced)                          |

### Outputs

| Parameter         | Type            | Description                               |
|-------------------|-----------------|-------------------------------------------|
| `WORKFLOW_CONFIG` | WORKFLOW_CONFIG | Workflow config object for context nodes  |
| `SEED`            | INT             | Generation seed                           |
| `STEPS`           | INT             | Number of sampling steps                  |
| `CFG`             | FLOAT           | Guidance scale                            |
| `SAMPLER_NAME`    | STRING          | Sampler algorithm name                    |
| `SCHEDULER`       | STRING          | Noise schedule name                       |
| `ASCORE_POSITIVE` | FLOAT           | Aesthetic score for positive conditioning |
| `ASCORE_NEGATIVE` | FLOAT           | Aesthetic score for negative conditioning |
| `WIDTH`           | INT             | Image width                               |
| `HEIGHT`          | INT             | Image height                              |
| `TARGET_WIDTH`    | INT             | CLIP target width                         |
| `TARGET_HEIGHT`   | INT             | CLIP target height                        |

### Usage

Connect `WORKFLOW_CONFIG` to context-based nodes. Use individual outputs for direct connections to sampler and encoder nodes. Set `target_width` and
`target_height` to match the original training resolution for best results — defaults to image dimensions if not set.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
