# TT_FluxWorkflowSettings

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Node for configuring Flux workflow generation parameters.

## Inputs

| Parameter      | Type   | Default | Range       | Description                          |
|----------------|--------|---------|-------------|--------------------------------------|
| `seed`         | INT    | 0       | 0 - 2^64-1  | Seed for reproducible results        |
| `steps`        | INT    | 25      | 1 - 10000   | Number of sampling steps             |
| `cfg`          | FLOAT  | 1.5     | 0.0 - 100.0 | CFG scale (classifier-free guidance) |
| `sampler_name` | STRING | -       | -           | Sampler name from available list     |
| `scheduler`    | STRING | -       | -           | Scheduler type                       |
| `guidance`     | FLOAT  | 3.5     | 1.0 - 10.0  | Guidance strength for Flux           |

## Outputs

| Output            | Type               | Description                  |
|-------------------|--------------------|------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Dictionary with all settings |
| `SEED`            | INT                | Seed value                   |
| `STEPS`           | INT                | Number of steps              |
| `CFG`             | FLOAT              | CFG scale                    |
| `SAMPLER_NAME`    | STRING             | Sampler name                 |
| `SCHEDULER`       | STRING             | Scheduler                    |
| `GUIDANCE`        | FLOAT              | Guidance value               |

## Purpose

Centralized control of generation settings for Flux models. Allows you to set all main parameters in one place and pass
them through the workflow both as a single config object and as individual values.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
