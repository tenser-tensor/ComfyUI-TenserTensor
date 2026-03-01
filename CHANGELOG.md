[1.5.11] - 2026-03-01
Added

New context nodes (API V3): Base Context, Context, FLUX2 Context, Passthrough, Set Guider / Image / Latent, Extract Encoder / Guided Sampler / VAE / Image for FLUX2
TT_LatentFactoryNode — V3 replacement for TT_LatentFactory
TT_Flux2WorkflowSettingsNode and TT_Flux2WorkflowSettingsAdvancedNode — V3 replacements for FLUX2 workflow settings nodes

Changed

Migrated node registration to explicit imports, replaced wildcard from .module import *
Per-group NODES_COUNT tracking and isolated error handling on import failures

Deprecated

All pre-V3 context, latent, and FLUX2 workflow nodes moved to Deprecated/ categories. Will be removed in a future major release.

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
