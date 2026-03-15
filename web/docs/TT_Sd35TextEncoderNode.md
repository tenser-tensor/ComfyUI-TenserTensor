## TT SD3.5 Text Encoder *TT_Sd35TextEncoderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Encodes text prompts for SD3.5 using all three text encoders (CLIP-L, CLIP-G, T5-XXL) and returns a configured Guider object ready for sampling.

### Inputs

| Parameter         | Type   | Required | Description                                               |
|-------------------|--------|----------|-----------------------------------------------------------|
| `model`           | MODEL  | Yes      | SD3.5 diffusion model                                     |
| `clip`            | CLIP   | Yes      | SD3.5 text encoders (CLIP-L, CLIP-G, T5-XXL)              |
| `cfg`             | FLOAT  | No       | Classifier-free guidance scale. Default: `5.0`            |
| `clip_l_positive` | STRING | No       | Positive prompt for CLIP-L encoder                        |
| `clip_g_positive` | STRING | No       | Positive prompt for CLIP-G encoder                        |
| `t5xxl_positive`  | STRING | No       | Positive prompt for T5-XXL encoder                        |
| `clip_l_negative` | STRING | No       | Negative prompt for CLIP-L encoder                        |
| `clip_g_negative` | STRING | No       | Negative prompt for CLIP-G encoder                        |
| `t5xxl_negative`  | STRING | No       | Negative prompt for T5-XXL encoder                        |
| `lora_triggers`   | STRING | No       | LoRA trigger words appended to positive prompts           |
| `width`           | INT    | No       | Output width for resolution conditioning. Default: `512`  |
| `height`          | INT    | No       | Output height for resolution conditioning. Default: `512` |
| `target_width`    | INT    | No       | Target width for resolution conditioning. Default: `512`  |
| `target_height`   | INT    | No       | Target height for resolution conditioning. Default: `512` |

### Outputs

| Parameter | Type   | Description                                             |
|-----------|--------|---------------------------------------------------------|
| `GUIDER`  | GUIDER | Configured guider with encoded conditioning for sampler |

### Usage

Connect `MODEL` and `CLIP` from a SD3.5 models loader node. Connect `GUIDER` to a sampler node. Use different prompts per encoder for fine-grained
control — T5-XXL handles long descriptive prompts best, CLIP-L and CLIP-G work better with short style tags.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
