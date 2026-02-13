## TT SDXL Workflow Settings (Advanced) *TT_SdxlWorkflowSettingsAdvanced*

Advanced SDXL workflow configuration with separate CLIP-L/G prompts and aesthetic scores.

### Inputs

| Parameter         | Type      | Required | Description                                             |
|-------------------|-----------|----------|---------------------------------------------------------|
| `seed`            | INT       | Yes      | Random seed (0 to 2^64-1, default: 0)                   |
| `steps`           | INT       | Yes      | Sampling steps (1-10000, default: 30)                   |
| `cfg`             | FLOAT     | Yes      | CFG scale (0.0-100.0, default: 7.0)                     |
| `sampler_name`    | SAMPLER   | Yes      | Sampler algorithm                                       |
| `scheduler`       | SCHEDULER | Yes      | Noise scheduler                                         |
| `clip_l_positive` | STRING    | Yes      | CLIP-L positive prompt (multiline)                      |
| `clip_g_positive` | STRING    | Yes      | CLIP-G positive prompt (multiline)                      |
| `clip_l_negative` | STRING    | Yes      | CLIP-L negative prompt (multiline)                      |
| `clip_g_negative` | STRING    | Yes      | CLIP-G negative prompt (multiline)                      |
| `ascore_positive` | FLOAT     | Yes      | Aesthetic score for positive (0.0-1000.0, default: 9.0) |
| `ascore_negative` | FLOAT     | Yes      | Aesthetic score for negative (0.0-1000.0, default: 6.0) |
| `width`           | INT       | Yes      | Image width (default: 512)                              |
| `height`          | INT       | Yes      | Image height (default: 512)                             |
| `target_width`    | INT       | Yes      | Target width for conditioning (default: 512)            |
| `target_height`   | INT       | Yes      | Target height for conditioning (default: 512)           |

### Outputs

| Parameter         | Type               | Description                                |
|-------------------|--------------------|--------------------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Complete workflow configuration dictionary |
| `SEED`            | INT                | Random seed                                |
| `STEPS`           | INT                | Sampling steps                             |
| `CFG`             | FLOAT              | CFG scale                                  |
| `SAMPLER_NAME`    | STRING             | Sampler name                               |
| `SCHEDULER`       | STRING             | Scheduler name                             |
| `CLIP_L_POSITIVE` | STRING             | CLIP-L positive prompt                     |
| `CLIP_G_POSITIVE` | STRING             | CLIP-G positive prompt                     |
| `CLIP_L_NEGATIVE` | STRING             | CLIP-L negative prompt                     |
| `CLIP_G_NEGATIVE` | STRING             | CLIP-G negative prompt                     |
| `ASCORE_POSITIVE` | FLOAT              | Aesthetic score positive                   |
| `ASCORE_NEGATIVE` | FLOAT              | Aesthetic score negative                   |
| `WIDTH`           | INT                | Width                                      |
| `HEIGHT`          | INT                | Height                                     |
| `TARGET_WIDTH`    | INT                | Target width                               |
| `TARGET_HEIGHT`   | INT                | Target height                              |

### Usage

Configure all SDXL workflow parameters with fine-grained control over CLIP-L and CLIP-G prompts separately, plus
aesthetic scores and target dimensions. Returns both a bundled config dictionary and individual parameters for flexible
workflow design.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
