## TT SD3.5 GGUF Workflow Settings *TT_Sd35GgufWorkflowSettingsNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Configures sampling parameters for SD3.5 pipelines. Builds a workflow config object, sampler, and SD3.5-specific sigmas in a single node.

### Inputs

| Parameter        | Type  | Required | Description                                                     |
|------------------|-------|----------|-----------------------------------------------------------------|
| `seed`           | INT   | No       | Sampling seed. Default: `0`                                     |
| `steps`          | INT   | No       | Number of denoising steps. Default: `30`, range: `1` to `10000` |
| `cfg`            | FLOAT | No       | Classifier-free guidance scale. Default: `5.0`                  |
| `sampler_name`   | COMBO | Yes      | Sampler algorithm                                               |
| `schedule_shift` | FLOAT | No       | Sigma schedule shift. Default: `3.0`, range: `0.0` to `20.0`    |
| `width`          | INT   | No       | Output width in pixels. Default: `1024`, step: `8`              |
| `height`         | INT   | No       | Output height in pixels. Default: `1024`, step: `8`             |
| `target_width`   | INT   | No       | Target width for resolution conditioning. Default: `1024`       |
| `target_height`  | INT   | No       | Target height for resolution conditioning. Default: `1024`      |

### Outputs

| Parameter         | Type               | Description                             |
|-------------------|--------------------|-----------------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Workflow configuration object           |
| `SAMPLER`         | SAMPLER            | Configured sampler                      |
| `SIGMAS`          | SIGMAS             | SD3.5 noise schedule with shift applied |
| `SEED`            | INT                | Seed passthrough                        |
| `STEPS`           | INT                | Steps passthrough                       |
| `CFG`             | FLOAT              | CFG passthrough                         |
| `WIDTH`           | INT                | Width passthrough                       |
| `HEIGHT`          | INT                | Height passthrough                      |
| `TARGET_WIDTH`    | INT                | Target width passthrough                |
| `TARGET_HEIGHT`   | INT                | Target height passthrough               |

### Usage

Connect outputs to a SD3.5 text encoder context node. Use `target_width` and `target_height` to match the resolution the model was trained on when
generating at non-standard sizes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
