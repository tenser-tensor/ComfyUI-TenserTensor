## TT Flux2 Workflow Settings *TT_Flux2WorkflowSettings*

⚠️ Deprecated: This node will be removed in a future major release. Please migrate to the new context nodes.

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Central workflow configuration node for FLUX2 pipelines. Consolidates all sampling parameters into a single
TT_WORKFLOW_CONFIG object while also exposing each value as an individual output.

### Inputs

| Parameter      | Type   | Required | Description                                                               |
|----------------|--------|----------|---------------------------------------------------------------------------|
| `seed`         | INT    | Yes      | Generation seed (0 – 18446744073709551615, default: 0)                    |
| `steps`        | INT    | Yes      | Number of sampling steps (1–10000, default: 25)                           |
| `cfg`          | FLOAT  | Yes      | CFG scale (0.0–100.0, default: 1.5)                                       |
| `sampler_name` | STRING | Yes      | Sampler algorithm (KSampler sampler list)                                 |
| `width`        | INT    | Yes      | Output image width in pixels (16–MAX_RESOLUTION, step: 8, default: 1024)  |
| `height`       | INT    | Yes      | Output image height in pixels (16–MAX_RESOLUTION, step: 8, default: 1024) |
| `guidance`     | FLOAT  | Yes      | Guidance scale for text encoder (1.0–10.0, default: 3.5)                  |

### Outputs

| Parameter         | Type               | Description                                          |
|-------------------|--------------------|------------------------------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Full configuration object with all settings bundled  |
| `SEED`            | INT                | Generation seed                                      |
| `STEPS`           | INT                | Number of sampling steps                             |
| `CFG`             | FLOAT              | CFG scale                                            |
| `SAMPLER`         | SAMPLER            | Instantiated sampler object                          |
| `SAMPLER_NAME`    | STRING             | Name of the selected sampler                         |
| `SCHEDULER`       | SIGMAS             | Computed sigma schedule based on seed and resolution |
| `WIDTH`           | INT                | Output image width                                   |
| `HEIGHT`          | INT                | Output image height                                  |
| `GUIDANCE`        | FLOAT              | Guidance scale                                       |

### Usage

Use this node as the single source of truth for FLUX2 workflow parameters. The `WORKFLOW_CONFIG` output is
designed for context-aware nodes that consume a TT_WORKFLOW_CONFIG directly. Individual outputs are available
for connecting to standard ComfyUI nodes. The sigma schedule (`SCHEDULER`) is computed automatically from
the seed and resolution via `get_schedule`.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
