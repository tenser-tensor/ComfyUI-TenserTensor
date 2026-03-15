## TT LTX2.3 Text Encoder *TT_Ltx23TextEncoderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes text prompts for LTX-Video 2.3 using Gemma 3 12B and returns a configured Guider object ready for sampling.

### Inputs

| Parameter         | Type   | Required | Description                                                                   |
|-------------------|--------|----------|-------------------------------------------------------------------------------|
| `model`           | MODEL  | Yes      | LTX2.3 diffusion model                                                        |
| `clip`            | CLIP   | Yes      | Gemma 3 12B text encoder                                                      |
| `cfg`             | FLOAT  | No       | Classifier-free guidance scale. Default: `1.0`. Use `1.0` with distilled LoRA |
| `positive_prompt` | STRING | No       | Positive text prompt                                                          |
| `negative_prompt` | STRING | No       | Negative text prompt                                                          |
| `lora_triggers`   | STRING | No       | LoRA trigger words appended to positive prompt                                |
| `frame_rate`      | COMBO  | No       | Frame rate used for conditioning. Default: `24fps`                            |

### Outputs

| Parameter | Type   | Description                                             |
|-----------|--------|---------------------------------------------------------|
| `GUIDER`  | GUIDER | Configured guider with encoded conditioning for sampler |

### Usage

Connect `MODEL` and `CLIP` from a models loader node. Connect `GUIDER` output to a sampler node. Use `cfg=1.0` when using distilled LoRA.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
