## TT Context Extract Encoder FLUX2 *TT_ContextExtractEncoderFlux2*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extracts model, clip, prompt, LoRA triggers, and guidance from the context for direct connection to a FLUX2
text encoder node.

### Inputs

| Parameter | Type       | Required | Description    |
|-----------|------------|----------|----------------|
| `context` | TT_CONTEXT | Yes      | Context object |

### Outputs

| Parameter       | Type       | Description                     |
|-----------------|------------|---------------------------------|
| `CONTEXT`       | TT_CONTEXT | Passthrough context object      |
| `MODEL`         | MODEL      | Diffusion model                 |
| `CLIP`          | CLIP       | CLIP text encoder               |
| `PROMPT`        | STRING     | Main generation prompt          |
| `LORA_TRIGGERS` | STRING     | LoRA trigger words              |
| `GUIDANCE`      | FLOAT      | Guidance scale for text encoder |

### Usage

Use this node to extract encoding parameters from the context and connect them directly to a FLUX2 text
encoder node without manually routing each wire.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
