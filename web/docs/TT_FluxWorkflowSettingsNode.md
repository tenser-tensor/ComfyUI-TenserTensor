## TT FLUX Workflow Settings *TT_FluxWorkflowSettingsNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Configures global workflow parameters for FLUX pipelines. Outputs a workflow config object alongside individual parameters for direct node
connections.

### Inputs

| Parameter      | Type  | Required | Description                          |
|----------------|-------|----------|--------------------------------------|
| `seed`         | INT   | Yes      | Generation seed                      |
| `steps`        | INT   | Yes      | Number of sampling steps, default 30 |
| `cfg`          | FLOAT | Yes      | Guidance scale, default 5.0          |
| `sampler_name` | COMBO | Yes      | Sampler algorithm                    |
| `scheduler`    | COMBO | Yes      | Noise schedule                       |
| `guidance`     | FLOAT | Yes      | FLUX guidance scale, default 3.0     |

### Outputs

| Parameter         | Type            | Description                              |
|-------------------|-----------------|------------------------------------------|
| `WORKFLOW_CONFIG` | WORKFLOW_CONFIG | Workflow config object for context nodes |
| `SEED`            | INT             | Generation seed                          |
| `STEPS`           | INT             | Number of sampling steps                 |
| `CFG`             | FLOAT           | Guidance scale                           |
| `SAMPLER_NAME`    | STRING          | Sampler algorithm name                   |
| `SCHEDULER`       | STRING          | Noise schedule name                      |
| `GUIDANCE`        | FLOAT           | FLUX guidance scale                      |

### Usage

Connect `WORKFLOW_CONFIG` to context-based nodes. Use individual outputs for direct connections to sampler and encoder nodes. `guidance` controls the
FLUX-specific distilled guidance — recommended range is 1.0–5.0.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
