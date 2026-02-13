# TT FLUX Workflow Settings (Advanced) *TT_FluxWorkflowSettingsAdvanced*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Advanced node for configuring Flux workflow generation parameters with separate CLIP-L and T5XXL prompts.

## Inputs

| Parameter         | Type   | Default | Range       | Description                          |
|-------------------|--------|---------|-------------|--------------------------------------|
| `seed`            | INT    | 0       | 0 - 2^64-1  | Seed for reproducible results        |
| `steps`           | INT    | 25      | 1 - 10000   | Number of sampling steps             |
| `cfg`             | FLOAT  | 1.5     | 0.0 - 100.0 | CFG scale (classifier-free guidance) |
| `sampler_name`    | STRING | -       | -           | Sampler name from available list     |
| `scheduler`       | STRING | -       | -           | Scheduler type                       |
| `clip_l_positive` | STRING | -       | -           | Positive prompt for CLIP-L encoder   |
| `t5xxl_positive`  | STRING | -       | -           | Positive prompt for T5XXL encoder    |
| `clip_l_negative` | STRING | -       | -           | Negative prompt for CLIP-L encoder   |
| `t5xxl_negative`  | STRING | -       | -           | Negative prompt for T5XXL encoder    |
| `guidance`        | FLOAT  | 3.5     | 1.0 - 10.0  | Guidance strength for Flux           |

## Outputs

| Output            | Type               | Description                  |
|-------------------|--------------------|------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Dictionary with all settings |
| `SEED`            | INT                | Seed value                   |
| `STEPS`           | INT                | Number of steps              |
| `CFG`             | FLOAT              | CFG scale                    |
| `SAMPLER_NAME`    | STRING             | Sampler name                 |
| `SCHEDULER`       | STRING             | Scheduler                    |
| `CLIP_L_POSITIVE` | STRING             | CLIP-L positive prompt       |
| `T5XXL_POSITIVE`  | STRING             | T5XXL positive prompt        |
| `CLIP_L_NEGATIVE` | STRING             | CLIP-L negative prompt       |
| `T5XXL_NEGATIVE`  | STRING             | T5XXL negative prompt        |
| `GUIDANCE`        | FLOAT              | Guidance value               |

## Purpose

Extended version of Flux workflow settings with dual-encoder prompt control. Allows separate configuration of CLIP-L and
T5XXL text encoders for precise control over the generation process. Supports dynamic prompts and multiline text input.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
