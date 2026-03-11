# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from typing import override

import latent_preview
from comfy import sample, model_management
from comfy_api.latest import ComfyExtension, io
from .nodes_latent import SCALE_FACTORS, SCALE_METHODS, scale_latent
from .nodes_text_encoder import SingleCondCFGGuider

CATEGORY = "TenserTensor/Sampling"


def execute_guided_sampling(**kwargs):
    guider, latent, sigmas, random_noise, sampler, preview_latent = (
        kwargs.get("guider"),
        kwargs.get("latent"),
        kwargs.get("sigmas"),
        kwargs.get("random_noise"),
        kwargs.get("sampler"),
        kwargs.get("preview_latent"),
    )

    if not isinstance(guider, SingleCondCFGGuider):
        guider = SingleCondCFGGuider.from_cfg_guider(guider)

    model_patcher = guider.model_patcher
    latent_dict = latent.copy()
    latent_tensor = sample.fix_empty_latent_channels(
        model_patcher,
        latent_dict["samples"],
        latent.get("downscale_ratio_spacial", None)
    )
    latent_dict["samples"] = latent_tensor
    noise_mask = latent.get("noise_mask", None)
    interim_buffer = {}
    if preview_latent:
        latent_preview.set_preview_method("latent2rgb")
        callback = latent_preview.prepare_callback(model_patcher, sigmas.shape[-1] - 1, interim_buffer)
    else:
        callback = None
    # disable_progress_bar = not utils.PROGRESS_BAR_ENABLED

    samples = guider.sample(
        random_noise.generate_noise(latent),
        latent_tensor,
        sampler,
        sigmas,
        denoise_mask=noise_mask,
        callback=callback,
        disable_pbar=False,
        seed=random_noise.seed
    ).to(model_management.intermediate_device())

    sampled_latent = latent_dict.copy()
    sampled_latent.pop("downscale_ratio_spacial", None)
    sampled_latent["samples"] = samples

    return sampled_latent


class TT_GuidedKSamplerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_GuidedKSamplerNode",
            display_name="TT Guided KSampler",
            category=CATEGORY,
            description="",
            inputs=[
                io.Latent.Input("latent"),
                io.Guider.Input("guider"),
                io.Sigmas.Input("sigmas"),
                io.Sampler.Input("sampler"),
                io.Noise.Input("random_noise"),
            ],
            outputs=[
                io.Latent.Output("SAMPLES")
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        samples = execute_guided_sampling(**kwargs)

        return io.NodeOutput(samples)


class TT_GuidedUpscaleKSamplerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_GuidedUpscaleKSamplerNode",
            display_name="TT Guided Upscale KSampler",
            category=CATEGORY,
            description="",
            inputs=[
                io.Latent.Input("latent"),
                io.Guider.Input("guider"),
                io.Sigmas.Input("sigmas"),
                io.Sampler.Input("sampler"),
                io.Noise.Input("random_noise"),
                io.Boolean.Input("scale_latent", default=False, label_on="Scale", label_off="Skip"),
                io.Combo.Input("scale_factor", options=SCALE_FACTORS, default="1x", advanced=True),
                io.Combo.Input("scale_method", options=SCALE_METHODS, default="bicubic", advanced=True),
            ],
            outputs=[
                io.Latent.Output("SAMPLES")
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        samples = execute_guided_sampling(**kwargs)

        if kwargs.get("scale_latent"):
            samples = scale_latent(**kwargs)

        return io.NodeOutput(samples)


class TT_GuidedKSamplerWithPreviewNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_GuidedKSamplerWithPreviewNode",
            display_name="TT Guided KSampler (With Preview)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Latent.Input("latent"),
                io.Guider.Input("guider"),
                io.Sigmas.Input("sigmas"),
                io.Sampler.Input("sampler"),
                io.Noise.Input("random_noise"),
                io.Boolean.Input("preview_latent", default=True, label_on="Show Peview", label_off="Only Sample"),
            ],
            outputs=[
                io.Latent.Output("SAMPLES")
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        samples = execute_guided_sampling(**kwargs)

        return io.NodeOutput(samples)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

class SamplingNodesExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            TT_GuidedKSamplerNode,
            TT_GuidedUpscaleKSamplerNode,
            TT_GuidedKSamplerWithPreviewNode,
        ]


async def comfy_entrypoint() -> SamplingNodesExtension:
    return SamplingNodesExtension()


# ==============================================================================
# Re-exports for backward compatibility
# ==============================================================================

__all__ = [
    "TT_GuidedKSamplerNode",
    "TT_GuidedUpscaleKSamplerNode",
    "TT_GuidedKSamplerWithPreviewNode",
]
