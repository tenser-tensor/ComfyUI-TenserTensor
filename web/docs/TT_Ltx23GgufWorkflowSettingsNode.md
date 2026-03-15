## TT LTX2.3 GGUF Workflow Settings *TT_Ltx23GgufWorkflowSettingsNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Configures sampling parameters for LTX-Video 2.3 pipelines. Builds a workflow config object, sampler, and LTX-specific sigmas in a single node.

### Inputs

| Parameter      | Type   | Required | Description                                                                   |
|----------------|--------|----------|-------------------------------------------------------------------------------|
| `latent_opt`   | LATENT | No       | Optional latent input for resolution-aware sigma calculation                  |
| `seed`         | INT    | No       | Sampling seed. Default: `0`                                                   |
| `steps`        | INT    | No       | Number of denoising steps. Default: `20`, range: `1` to `10000`               |
| `cfg`          | FLOAT  | No       | Classifier-free guidance scale. Default: `1.0`. Use `1.0` with distilled LoRA |
| `sampler_name` | COMBO  | Yes      | Sampler algorithm                                                             |
| `frame_rate`   | COMBO  | No       | Frame rate. Default: `24fps`                                                  |
| `width`        | INT    | No       | Output width in pixels. Default: `1024`, step: `8`                            |
| `height`       | INT    | No       | Output height in pixels. Default: `1024`, step: `8`                           |

### Outputs

| Parameter         | Type               | Description                                           |
|-------------------|--------------------|-------------------------------------------------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Workflow configuration object for context-based nodes |
| `SAMPLER`         | SAMPLER            | Configured sampler                                    |
| `SIGMAS`          | SIGMAS             | LTX-specific noise schedule                           |
| `SEED`            | INT                | Seed passthrough                                      |
| `CFG`             | FLOAT              | CFG scale passthrough                                 |
| `WIDTH`           | INT                | Width passthrough                                     |
| `HEIGHT`          | INT                | Height passthrough                                    |
| `FRAME_RATE`      | COMBO              | Frame rate passthrough                                |

### Usage

Connect `WIDTH`, `HEIGHT` and `FRAME_RATE` from a latent factory node. Connect `SAMPLER` and `SIGMAS` to a sampler node. Use `CFG=1.0` when using
distilled LoRA.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
