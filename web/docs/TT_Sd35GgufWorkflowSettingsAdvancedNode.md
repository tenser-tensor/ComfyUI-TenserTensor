## TT SD3.5 GGUF Workflow Settings (Advanced) *TT_Sd35GgufWorkflowSettingsAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Configures sampling parameters for SD3.5 pipelines with full control over all three text encoders, sigma schedule shift, and target resolution
conditioning.

### Inputs

| Parameter         | Type   | Required | Description                                                     |
|-------------------|--------|----------|-----------------------------------------------------------------|
| `seed`            | INT    | No       | Sampling seed. Default: `0`                                     |
| `steps`           | INT    | No       | Number of denoising steps. Default: `30`, range: `1` to `10000` |
| `cfg`             | FLOAT  | No       | Classifier-free guidance scale. Default: `5.0`                  |
| `sampler_name`    | COMBO  | Yes      | Sampler algorithm                                               |
| `schedule_shift`  | FLOAT  | No       | Sigma schedule shift. Default: `3.0`, range: `0.0` to `20.0`    |
| `clip_l_positive` | STRING | No       | Positive prompt for CLIP-L encoder                              |
| `clip_g_positive` | STRING | No       | Positive prompt for CLIP-G encoder                              |
| `t5xxl_positive`  | STRING | No       | Positive prompt for T5-XXL encoder                              |
| `clip_l_negative` | STRING | No       | Negative prompt for CLIP-L encoder                              |
| `clip_g_negative` | STRING | No       | Negative prompt for CLIP-G encoder                              |
| `t5xxl_negative`  | STRING | No       | Negative prompt for T5-XXL encoder                              |
| `lora_triggers`   | STRING | No       | LoRA trigger words appended to positive prompts                 |
| `width`           | INT    | No       | Output width in pixels. Default: `1024`, step: `8`              |
| `height`          | INT    | No       | Output height in pixels. Default: `1024`, step: `8`             |
| `target_width`    | INT    | No       | Target width for resolution conditioning. Default: `1024`       |
| `target_height`   | INT    | No       | Target height for resolution conditioning. Default: `1024`      |

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
| `CLIP_L_POSITIVE` | STRING             | CLIP-L positive prompt passthrough      |
| `CLIP_G_POSITIVE` | STRING             | CLIP-G positive prompt passthrough      |
| `T5XXL_POSITIVE`  | STRING             | T5-XXL positive prompt passthrough      |
| `CLIP_L_NEGATIVE` | STRING             | CLIP-L negative prompt passthrough      |
| `CLIP_G_NEGATIVE` | STRING             | CLIP-G negative prompt passthrough      |
| `T5XXL_NEGATIVE`  | STRING             | T5-XXL negative prompt passthrough      |
| `LORA_TRIGGERS`   | STRING             | LoRA triggers passthrough               |

### Usage

Connect outputs to a SD3.5 text encoder context node. Use different prompts per encoder for fine-grained control — T5-XXL handles long descriptive
prompts best, CLIP-L and CLIP-G work better with short style tags.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
