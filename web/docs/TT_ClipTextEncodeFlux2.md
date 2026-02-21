## TT Clip Text Encode Flux2 *TT_ClipTextEncodeFlux2*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Text prompt encoder for FLUX2 models with LoRA trigger word support and built-in guidance configuration.

### Inputs

| Parameter       | Type   | Required | Description                                                  |
|-----------------|--------|----------|--------------------------------------------------------------|
| `model`         | MODEL  | Yes      | Diffusion model                                              |
| `clip`          | CLIP   | Yes      | CLIP model for text encoding                                 |
| `prompt`        | STRING | Yes      | Main generation prompt (multiline, supports dynamic prompts) |
| `lora_triggers` | STRING | Yes      | LoRA trigger words (multiline, supports dynamic prompts)     |
| `guidance`      | FLOAT  | Yes      | Guidance scale for generation (1.0–10.0, default: 3.5)       |

### Outputs

| Parameter | Type   | Description                                        |
|-----------|--------|----------------------------------------------------|
| `GUIDER`  | GUIDER | Configured guider with encoded prompt and guidance |

### Usage

Encodes text prompts specifically for FLUX2 models. Enter your main prompt in `prompt` and any LoRA-specific trigger
words separately in `lora_triggers` — the node combines them internally. Adjust `guidance` to control how strongly
the model follows the prompt (3.5 is a good starting point for FLUX2).

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
