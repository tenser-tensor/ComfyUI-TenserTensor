## TT FLUX2 Workflow Settings *TT_Flux2WorkflowSettingsNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Workflow configuration node for FLUX2 pipelines. Bundles all sampling parameters into a single
TT_WORKFLOW_CONFIG object and computes sampler and sigma schedule automatically.

### Inputs

| Parameter      | Type  | Required | Description                                                               |
|----------------|-------|----------|---------------------------------------------------------------------------|
| `seed`         | INT   | Yes      | Generation seed (0 – 18446744073709551615, default: 0)                    |
| `steps`        | INT   | Yes      | Number of sampling steps (1–10000, default: 30)                           |
| `cfg`          | FLOAT | Yes      | CFG scale (0.0–100.0, default: 3.0)                                       |
| `guidance`     | FLOAT | Yes      | Guidance scale for text encoder (1.0–10.0, default: 3.0)                  |
| `width`        | INT   | Yes      | Output image width in pixels (16–MAX_RESOLUTION, step: 8, default: 1024)  |
| `height`       | INT   | Yes      | Output image height in pixels (16–MAX_RESOLUTION, step: 8, default: 1024) |
| `sampler_name` | COMBO | Yes      | Sampler algorithm (KSampler sampler list)                                 |

### Outputs

| Parameter         | Type               | Description                                           |
|-------------------|--------------------|-------------------------------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Full configuration object with all settings bundled   |
| `SAMPLER`         | SAMPLER            | Instantiated sampler object                           |
| `SIGMAS`          | SIGMAS             | Computed sigma schedule based on steps and resolution |
| `SEED`            | INT                | Generation seed                                       |
| `STEPS`           | INT                | Number of sampling steps                              |
| `CFG`             | FLOAT              | CFG scale                                             |
| `GUIDANCE`        | FLOAT              | Guidance scale                                        |
| `WIDTH`           | INT                | Output image width                                    |
| `HEIGHT`          | INT                | Output image height                                   |

### Usage

Use this node as the single source of truth for FLUX2 workflow parameters. The sampler and sigma schedule
are computed automatically from the selected sampler, step count, and resolution. Connect `WORKFLOW_CONFIG`
to context nodes, or use individual outputs to connect to standard ComfyUI nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
