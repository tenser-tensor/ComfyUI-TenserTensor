## TT Clip Text Encode Flux2 (Context) *TT_ClipTextEncodeFlux2Context*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Context-based text prompt encoder for FLUX2 models. Extracts model, CLIP, and prompt configuration directly from a TT_CONTEXT object.

### Inputs

| Parameter | Type       | Required | Description                                                                           |
|-----------|------------|----------|---------------------------------------------------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object containing `model`, `clip`, and `workflow_config` with prompt settings |

### Outputs

| Parameter | Type       | Description                                        |
|-----------|------------|----------------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context with `guider` written back into it |
| `GUIDER`  | GUIDER     | Configured guider with encoded prompt and guidance |

### Usage

Context-aware version of the FLUX2 text encoder. Instead of individual inputs, it reads `model`, `clip`, and
`workflow_config` (containing `prompt`, `lora_triggers`, and `guidance`) from the passed `context`. The resulting
guider is both returned as an output and stored back into the context under the `guider` key. Raises an error if
any of the required fields are missing from the context.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
