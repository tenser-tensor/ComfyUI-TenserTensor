# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import torch

import latent_preview
from comfy import sample, model_management, samplers
from comfy_api.latest import io
from .nodes_context import Context
from .nodes_latent import scale_latent
from .nodes_text_encoder import SingleCondCFGGuider
from .utils import CommonTypes, raise_if

CATEGORY = "TenserTensor/Sampling"


def do_sample(**kwargs):
    model, latent = kwargs.get("model"), kwargs.get("latent")
    raise_if(model is None, ValueError, "MODEL is required for text encoder")
    raise_if(latent is None, ValueError, "LATENT is required for text encoder")

    latent_dict = latent.copy()
    samples, add_noise, seed, steps, device = (
        latent_dict["samples"],
        kwargs.get("add_noise", True),
        kwargs.get("seed", 0),
        kwargs.get("steps", 0),
        kwargs.get("device", "cpu")
    )
    latent_tensor = sample.fix_empty_latent_channels(model, samples, latent.get("downscale_ratio_spacial", None))

    if add_noise:
        batch_idx = latent.get("batch_index", None)
        noise = sample.prepare_noise(samples, seed, batch_idx)
    else:
        noise = torch.zeros(samples.size(), dtype=samples.dtype, layout=samples.layout, device="cpu")

    interim_buffer = {}
    if kwargs.get("preview_latent"):
        latent_preview.set_preview_method("latent2rgb")
        callback = latent_preview.prepare_callback(model, steps - 1, interim_buffer)
    else:
        callback = None

    args = {
        "model": model,
        "noise": noise,
        "steps": steps,
        "cfg": kwargs.get("cfg"),
        "sampler_name": kwargs.get("sampler_name"),
        "scheduler": kwargs.get("scheduler"),
        "positive": kwargs.get("positive"),
        "negative": kwargs.get("negative"),
        "latent_image": latent_tensor,
        "denoise": kwargs.get("denoise", 1.0),
        "disable_noise": not add_noise,
        "start_step": kwargs.get("start_step"),
        "last_step": kwargs.get("last_step"),
        "force_full_denoise": kwargs.get("full_denoise", True),
        "noise_mask": latent.get("noise_mask"),
        "callback": callback,
        "seed": seed,
    }

    samples = sample.sample(**args)
    sampled_latent = latent_dict.copy()
    sampled_latent.pop("downscale_ratio_spacial", None)
    sampled_latent["samples"] = samples

    return sampled_latent


class TT_KSamplerNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerNode",
            display_name="TT KSampler",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Conditioning.Input("positive"),
                io.Conditioning.Input("negative"),
                io.Latent.Input("latent"),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=samplers.KSampler.SAMPLERS),
                io.Combo.Input("scheduler", options=samplers.KSampler.SCHEDULERS),
                io.Boolean.Input("preview_latent", default=False, label_on="Show Preview", label_off="Only Sample"),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        latent = do_sample(**kwargs)

        return io.NodeOutput(latent)


class TT_KSamplerAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerAdvancedNode",
            display_name="TT KSampler (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Conditioning.Input("positive"),
                io.Conditioning.Input("negative"),
                io.Latent.Input("latent"),
                io.Boolean.Input("add_noise", default=False, label_on="Random Noise", label_off="Zero Noise"),
                io.Boolean.Input("full_denoise", default=False, label_on="Complete", label_off="Partial"),
                io.Float.Input("denoise", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.Int.Input("start_step", default=0, min=0, max=10_000),
                io.Int.Input("last_step", default=10_000, min=0, max=10_000),
                io.Combo.Input("sampler_name", options=samplers.KSampler.SAMPLERS),
                io.Combo.Input("scheduler", options=samplers.KSampler.SCHEDULERS),
                io.Boolean.Input("preview_latent", default=False, label_on="Show Preview", label_off="Only Sample"),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        latent = do_sample(**kwargs)

        return io.NodeOutput(latent)


class TT_KSamplerContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerContextNode",
            display_name="TT KSampler (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context"),
                io.Boolean.Input("preview_latent", default=False, label_on="Show Preview", label_off="Only Sample"),
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, context) -> io.NodeOutput:
        model, latent, workflow_config = context.get("model"), context.get("latent"), context.get("workflow_config")
        raise_if(model is None, ValueError, "MODEL is required for text encoder")
        raise_if(latent is None, ValueError, "LATENT is required for text encoder")
        raise_if(workflow_config is None, ValueError, "WORKFLOW CONFIG is required for text encoder")

        args = {
            "model": model,
            "positive": context.get_attr("positive"),
            "negative": context.get_attr("negative"),
            "latent": latent,
            "seed": workflow_config.get_attr("seed"),
            "steps": workflow_config.get_attr("steps"),
            "cfg": workflow_config.get_attr("cfg"),
            "sampler_name": workflow_config.get_attr("sampler_name"),
            "scheduler": workflow_config.get_attr("scheduler"),
        }
        latent = do_sample(**args)
        context.set_attr("latent", latent)

        return io.NodeOutput(context, latent)


class TT_KSamplerTwoStageNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_KSamplerTwoStageNode",
            display_name="TT KSampler (Two Stage)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Conditioning.Input("positive"),
                io.Conditioning.Input("negative"),
                io.Latent.Input("latent"),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.Int.Input("draft_steps", default=25, min=1, max=10_000),
                io.Int.Input("refiner_steps", default=25, min=1, max=10_000),
                io.Combo.Input("draft_sampler_name", options=samplers.KSampler.SAMPLERS),
                io.Combo.Input("draft_scheduler", options=samplers.KSampler.SCHEDULERS),
                io.Combo.Input("refiner_sampler_name", options=samplers.KSampler.SAMPLERS),
                io.Combo.Input("refiner_scheduler", options=samplers.KSampler.SCHEDULERS),
                io.Float.Input("draft_denoise", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Float.Input("refiner_denoise", default=1.0, min=0.0, max=1.0, step=0.01),
                io.Boolean.Input("preview_latent", default=False, label_on="Show Preview", label_off="Only Sample"),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        draft_steps = kwargs["draft_steps"]
        refiner_steps = kwargs["refiner_steps"]

        args = kwargs.copy()
        args.update({
            "steps": draft_steps,
            "start_step": 0,
            "add_noise": True,
            "sampler_name": kwargs["draft_sampler_name"],
            "scheduler": kwargs["draft_scheduler"],
            "full_denoise": False,
            "denoise": kwargs["draft_denoise"],
        })
        latent = do_sample(**args)

        args.update({
            "latent": latent,
            "steps": draft_steps + refiner_steps,
            "start_step": draft_steps,
            "add_noise": True,
            "sampler_name": kwargs["refiner_sampler_name"],
            "scheduler": kwargs["refiner_scheduler"],
            "full_denoise": True,
            "denoise": kwargs["refiner_denoise"],
        })
        latent = do_sample(**args)

        return io.NodeOutput(latent)


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
                io.Boolean.Input("preview_latent", default=False, label_on="Show Preview", label_off="Only Sample"),
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
                io.Combo.Input("scale_factor", options=CommonTypes.SCALE_FACTORS, default="1x", advanced=True),
                io.Combo.Input("scale_method", options=CommonTypes.SCALE_METHODS, default="bicubic", advanced=True),
                io.Boolean.Input("preview_latent", default=False, label_on="Show Preview", label_off="Only Sample"),
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


NODES = [
    TT_KSamplerNode,
    TT_KSamplerAdvancedNode,
    TT_KSamplerContextNode,
    TT_KSamplerTwoStageNode,
    TT_GuidedKSamplerNode,
    TT_GuidedUpscaleKSamplerNode,
]
