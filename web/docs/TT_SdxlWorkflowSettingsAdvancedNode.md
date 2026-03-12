## TT SDXL Workflow Settings (Advanced) *TT_SdxlWorkflowSettingsAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended SDXL workflow settings node with built-in prompt inputs for CLIP-L and CLIP-G encoders. Combines sampler configuration and text prompts in a
single node.

### Inputs

| Parameter         | Type   | Required | Description                                            |
|-------------------|--------|----------|--------------------------------------------------------|
| `seed`            | INT    | Yes      | Generation seed                                        |
| `steps`           | INT    | Yes      | Number of sampling steps, default 30                   |
| `cfg`             | FLOAT  | Yes      | Guidance scale, default 5.0                            |
| `sampler_name`    | COMBO  | Yes      | Sampler algorithm                                      |
| `scheduler`       | COMBO  | Yes      | Noise schedule                                         |
| `ascore_positive` | FLOAT  | Yes      | Aesthetic score for positive conditioning, default 9.0 |
| `ascore_negative` | FLOAT  | Yes      | Aesthetic score for negative conditioning, default 6.0 |
| `clip_l_positive` | STRING | Yes      | CLIP-L positive prompt                                 |
| `clip_g_positive` | STRING | Yes      | CLIP-G positive prompt                                 |
| `clip_l_negative` | STRING | Yes      | CLIP-L negative prompt                                 |
| `clip_g_negative` | STRING | Yes      | CLIP-G negative prompt                                 |
| `lora_triggers`   | STRING | No       | LoRA trigger words (advanced)                          |
| `width`           | INT    | Yes      | Image width in pixels                                  |
| `height`          | INT    | Yes      | Image height in pixels                                 |
| `target_width`    | INT    | No       | CLIP target width (advanced)                           |
| `target_height`   | INT    | No       | CLIP target height (advanced)                          |

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
| `CLIP_L_POSITIVE` | STRING          | CLIP-L positive prompt                    |
| `CLIP_G_POSITIVE` | STRING          | CLIP-G positive prompt                    |
| `CLIP_L_NEGATIVE` | STRING          | CLIP-L negative prompt                    |
| `CLIP_G_NEGATIVE` | STRING          | CLIP-G negative prompt                    |
| `LORA_TRIGGERS`   | STRING          | LoRA trigger words                        |
| `WIDTH`           | INT             | Image width                               |
| `HEIGHT`          | INT             | Image height                              |
| `TARGET_WIDTH`    | INT             | CLIP target width                         |
| `TARGET_HEIGHT`   | INT             | CLIP target height                        |

### Usage

Use when you want prompts and sampler settings in one place. Connect `WORKFLOW_CONFIG` to context nodes, or use individual outputs for direct
connections. LoRA trigger words are appended to the positive prompt automatically in the text encoder node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
