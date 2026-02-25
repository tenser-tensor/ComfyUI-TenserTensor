## v1.4.7 (2026-02-25)

### New Nodes
- **TT KSampler (Guided)** — guided diffusion sampling with external guider, sigmas, and sampler
- **TT Guider Image Reference** — encodes reference image into latent space and injects it into Guider conditioning
- **TT Image Preview / Upscale / Save** — all-in-one preview, upscale, and save node
- **TT FLUX2 GGUF Models Loader** / **(Advanced)** — loaders for FLUX2 GGUF-quantized models
- **TT CLIP Text Encode FLUX2** / **(Context)** — text encoders for FLUX2 models
- **TT FLUX2 Workflow Settings** / **(Advanced)** — workflow configuration nodes for FLUX2
- **TT Context Set Guider** — injects guider into TT_CONTEXT object

### Improvements
- Added `BasicGuider` and `CommonTypes` to shared lib (`lib/common.py`)
- Fixed missing f-strings in all error print statements across node imports
- Fixed workflow settings module filenames (typo: `workfow` → `workflow`)

### Docs
- Added docs for all new nodes
- Updated NODES.md with descriptions for all new nodes
- Updated Latent Factory description
