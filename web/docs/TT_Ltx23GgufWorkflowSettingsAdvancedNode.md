## TT LTX2.3 GGUF Workflow Settings (Advanced) *TT_Ltx23GgufWorkflowSettingsAdvancedNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extended version of TT LTX2.3 GGUF Workflow Settings with manual sigma schedule control, sigma stretching, and built-in prompt inputs.

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `latent_opt` | LATENT | No | Optional latent input for resolution-aware sigma calculation |
| `seed` | INT | No | Sampling seed. Default: `0` |
| `steps` | INT | No | Number of denoising steps. Default: `20`, range: `1` to `10000` |
| `cfg` | FLOAT | No | Classifier-free guidance scale. Default: `1.0`. Use `1.0` with distilled LoRA |
| `sampler_name` | COMBO | Yes | Sampler algorithm |
| `schedule_base_shift` | FLOAT | No | Base shift for sigma schedule. Default: `0.95` |
| `schedule_max_shift` | FLOAT | No | Max shift for sigma schedule. Default: `2.05` |
| `stretch_sigmas` | BOOLEAN | No | `In Range` — stretch sigmas to fill full range. `Bypass` — use as-is. Default: `In Range` |
| `sigmas_terminal` | FLOAT | No | Terminal sigma value when stretching. Default: `0.1` |
| `frame_rate` | COMBO | No | Frame rate. Default: `24fps` |
| `width` | INT | No | Output width in pixels. Default: `1024`, step: `8` |
| `height` | INT | No | Output height in pixels. Default: `1024`, step: `8` |
| `positive_prompt` | STRING | No | Positive text prompt |
| `negative_prompt` | STRING | No | Negative text prompt |
| `lora_triggers` | STRING | No | LoRA trigger words appended to positive prompt |

### Outputs

| Parameter | Type | Description |
|-----------|------|-------------|
| `WORKFLOW_CONFIG` | TT_WORKFLOW_CONFIG | Workflow configuration object for context-based nodes |
| `SAMPLER` | SAMPLER | Configured sampler |
| `SIGMAS` | SIGMAS | LTX-specific noise schedule |
| `SEED` | INT | Seed passthrough |
| `CFG` | FLOAT | CFG scale passthrough |
| `WIDTH` | INT | Width passthrough |
| `HEIGHT` | INT | Height passthrough |
| `POSITIVE_PROMPT` | STRING | Positive prompt passthrough |
| `NEGATIVE_PROMPT` | STRING | Negative prompt passthrough |
| `LORA_TRIGGERS` | STRING | LoRA triggers passthrough |
| `FRAME_RATE` | COMBO | Frame rate passthrough |

### Usage

Connect `WIDTH`, `HEIGHT` and `FRAME_RATE` from a latent factory node. Connect `SAMPLER` and `SIGMAS` to a sampler node. Use `CFG=1.0` with distilled LoRA. Adjust `schedule_base_shift` and `schedule_max_shift` to control noise schedule for different resolutions and durations.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
