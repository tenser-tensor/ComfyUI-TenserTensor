## TT FLUX Workflow Settings (Advanced) *TT_FluxWorkflowSettingsAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended FLUX workflow settings node with built-in prompt inputs for CLIP-L and T5-XXL encoders. Combines sampler configuration and text prompts in a
single node.

### Inputs

| Parameter         | Type   | Required | Description                          |
|-------------------|--------|----------|--------------------------------------|
| `seed`            | INT    | Yes      | Generation seed                      |
| `steps`           | INT    | Yes      | Number of sampling steps, default 30 |
| `cfg`             | FLOAT  | Yes      | Guidance scale, default 5.0          |
| `sampler_name`    | COMBO  | Yes      | Sampler algorithm                    |
| `scheduler`       | COMBO  | Yes      | Noise schedule                       |
| `clip_l_positive` | STRING | Yes      | CLIP-L positive prompt               |
| `t5xxl_positive`  | STRING | Yes      | T5-XXL positive prompt               |
| `clip_l_negative` | STRING | Yes      | CLIP-L negative prompt               |
| `t5xxl_negative`  | STRING | Yes      | T5-XXL negative prompt               |
| `lora_triggers`   | STRING | No       | LoRA trigger words (advanced)        |
| `guidance`        | FLOAT  | Yes      | FLUX guidance scale, default 3.0     |

### Outputs

| Parameter         | Type            | Description                              |
|-------------------|-----------------|------------------------------------------|
| `WORKFLOW_CONFIG` | WORKFLOW_CONFIG | Workflow config object for context nodes |
| `SEED`            | INT             | Generation seed                          |
| `STEPS`           | INT             | Number of sampling steps                 |
| `CFG`             | FLOAT           | Guidance scale                           |
| `SAMPLER_NAME`    | STRING          | Sampler algorithm name                   |
| `SCHEDULER`       | STRING          | Noise schedule name                      |
| `CLIP_L_POSITIVE` | STRING          | CLIP-L positive prompt                   |
| `T5XXL_POSITIVE`  | STRING          | T5-XXL positive prompt                   |
| `CLIP_L_NEGATIVE` | STRING          | CLIP-L negative prompt                   |
| `T5XXL_NEGATIVE`  | STRING          | T5-XXL negative prompt                   |
| `LORA_TRIGGERS`   | STRING          | LoRA trigger words                       |
| `GUIDANCE`        | FLOAT           | FLUX guidance scale                      |

### Usage

Use when you want prompts and sampler settings in one place. Connect `WORKFLOW_CONFIG` to context nodes, or use individual outputs for direct
connections. LoRA trigger words are appended to the positive prompt automatically in the text encoder node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
