## TT Flux2 Workflow Settings (Advanced) *TT_Flux2WorkflowSettingsAdvanced*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended workflow configuration node for FLUX2 pipelines. Includes all parameters from the base version plus
built-in prompt and LoRA trigger fields, bundling everything into a single TT_WORKFLOW_CONFIG object.

### Inputs

| Parameter       | Type   | Required | Description                                                               |
|-----------------|--------|----------|---------------------------------------------------------------------------|
| `seed`          | INT    | Yes      | Generation seed (0 – 18446744073709551615, default: 0)                    |
| `steps`         | INT    | Yes      | Number of sampling steps (1–10000, default: 25)                           |
| `cfg`           | FLOAT  | Yes      | CFG scale (0.0–100.0, default: 1.5)                                       |
| `sampler_name`  | STRING | Yes      | Sampler algorithm (KSampler sampler list)                                 |
| `width`         | INT    | Yes      | Output image width in pixels (16–MAX_RESOLUTION, step: 8, default: 1024)  |
| `height`        | INT    | Yes      | Output image height in pixels (16–MAX_RESOLUTION, step: 8, default: 1024) |
| `prompt`        | STRING | Yes      | Main generation prompt (multiline, supports dynamic prompts)              |
| `lora_triggers` | STRING | Yes      | LoRA trigger words (multiline, supports dynamic prompts)                  |
| `guidance`      | FLOAT  | Yes      | Guidance scale for text encoder (1.0–10.0, default: 3.5)                  |

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
| `PROMPT`          | STRING             | Main generation prompt                               |
| `GUIDANCE`        | FLOAT              | Guidance scale                                       |

### Usage

Advanced version of TT Flux2 Workflow Settings with `prompt` and `lora_triggers` fields included directly in the
node. Both are stored in the `WORKFLOW_CONFIG` output alongside all other sampling parameters, making this node
sufficient as the sole configuration source for full context-driven FLUX2 pipelines. Individual outputs remain
available for connecting to standard ComfyUI nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
