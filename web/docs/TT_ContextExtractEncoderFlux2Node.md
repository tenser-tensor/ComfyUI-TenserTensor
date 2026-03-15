## TT Context Extract Encoder (FLUX2) *TT_ContextExtractEncoderFlux2Node*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Extracts model, CLIP, and encoding parameters from a context object for use with a FLUX2 text encoder node.

### Inputs

| Parameter | Type       | Required | Description                                  |
|-----------|------------|----------|----------------------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object from an upstream context node |

### Outputs

| Parameter       | Type       | Description         |
|-----------------|------------|---------------------|
| `CONTEXT`       | TT_CONTEXT | Context passthrough |
| `MODEL`         | MODEL      | Diffusion model     |
| `CLIP`          | CLIP       | CLIP text encoder   |
| `PROMPT`        | STRING     | Text prompt         |
| `LORA_TRIGGERS` | STRING     | LoRA trigger words  |
| `GUIDANCE`      | FLOAT      | Guidance scale      |

### Usage

Connect `CONTEXT` from a FLUX2 context node. Connect outputs to a FLUX2 text encoder node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
