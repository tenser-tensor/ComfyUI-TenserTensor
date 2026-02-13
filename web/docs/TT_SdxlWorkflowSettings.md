# TT SDXL Workflow Settings *TT_SdxlWorkflowSettings*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Node for configuring SDXL workflow generation parameters.

## Inputs

| Parameter      | Type  | Default | Range       | Description                          |
|----------------|-------|---------|-------------|--------------------------------------|
| `seed`         | INT   | 0       | 0 - 2^64-1  | Seed for reproducible results        |
| `steps`        | INT   | 30      | 1 - 10000   | Number of sampling steps             |
| `cfg`          | FLOAT | 7.0     | 0.0 - 100.0 | CFG scale (classifier-free guidance) |
| `sampler_name` | COMBO | -       | -           | Sampler name from available list     |
| `scheduler`    | COMBO | -       | -           | Scheduler type                       |

## Outputs

| Output            | Type               | Description                  |
|-------------------|--------------------|------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Dictionary with all settings |
| `SEED`            | INT                | Seed value                   |
| `STEPS`           | INT                | Number of steps              |
| `CFG`             | FLOAT              | CFG scale                    |
| `SAMPLER_NAME`    | COMBO              | Sampler name                 |
| `SCHEDULER`       | COMBO              | Scheduler                    |

## Purpose

Centralized control of generation settings for SDXL models. Allows you to set all main parameters in one place and pass
them through the workflow both as a single config object and as individual values. Uses SDXL-optimized defaults (30
steps, CFG 7.0).

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
