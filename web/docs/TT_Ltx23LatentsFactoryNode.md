## TT LTX2.3 Latents Factory *TT_Ltx23LatentsFactoryNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Creates video and audio latent tensors for LTX-Video 2.3 pipelines. Optionally injects a reference image into the first frame of the video latent for
img2video workflows.

### Inputs

| Parameter            | Type    | Required | Description                                                                                                      |
|----------------------|---------|----------|------------------------------------------------------------------------------------------------------------------|
| `video_vae`          | VAE     | Yes      | Video VAE from models loader node                                                                                |
| `audio_vae`          | VAE     | Yes      | Audio VAE from models loader node                                                                                |
| `image_opt`          | IMAGE   | No       | Optional reference image for img2video                                                                           |
| `use_ref_frame`      | BOOLEAN | No       | `Inplace` — encode reference image into first video frame. `Bypass` — ignore reference image. Default: `Inplace` |
| `inplace_strength`   | FLOAT   | No       | Blend strength of reference frame. `1.0` — full reference, `0.0` — pure noise. Default: `0.7`                    |
| `inplace_scale_mode` | COMBO   | No       | Scaling method for reference image resize. Default: `bicubic`                                                    |
| `seed`               | INT     | No       | Seed for latent generation. Default: `0`                                                                         |
| `noise_seed`         | INT     | No       | Seed for sampler noise generator. Default: `0`                                                                   |
| `aspect_ratio`       | COMBO   | No       | Output aspect ratio. Default: `16:9`                                                                             |
| `megapixels`         | COMBO   | No       | Output resolution in megapixels. Default: `1 MP`                                                                 |
| `orientation`        | COMBO   | No       | `landscape` or `portrait`                                                                                        |
| `length_sec`         | INT     | No       | Video duration in seconds. Default: `5`, range: `1` to `20`                                                      |
| `frame_rate`         | COMBO   | No       | Frame rate. Default: `24fps`                                                                                     |
| `batch_size`         | INT     | No       | Number of latents in batch. Default: `1`                                                                         |

### Outputs

| Parameter      | Type   | Description                                         |
|----------------|--------|-----------------------------------------------------|
| `LATENT`       | LATENT | Combined video+audio latent for sampler             |
| `LATENT_VIDEO` | LATENT | Video latent for VAE decode or img2video transforms |
| `LATENT_AUDIO` | LATENT | Audio latent for VAE decode                         |
| `RND_NOISE`    | NOISE  | Noise generator for sampler                         |
| `SEED`         | INT    | Latent generation seed passthrough                  |
| `NOISE_SEED`   | INT    | Noise seed passthrough                              |
| `MEGAPIXELS`   | COMBO  | Megapixels passthrough                              |
| `FRAME_RATE`   | COMBO  | Frame rate passthrough                              |
| `WIDTH`        | INT    | Calculated output width in pixels                   |
| `HEIGHT`       | INT    | Calculated output height in pixels                  |

### Usage

Connect `VIDEO_VAE` and `AUDIO_VAE` from a models loader node. Connect `LATENT` and `RND_NOISE` to a sampler node. Use `LATENT_VIDEO` and
`LATENT_AUDIO` separately for VAE decode nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
