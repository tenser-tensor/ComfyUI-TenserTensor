# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import dataclasses
import math
from dataclasses import dataclass
from typing import override

import torch

from comfy.samplers import KSampler, sampler_object, Sampler
from comfy_api.latest import io, ComfyExtension
from nodes import MAX_RESOLUTION

CATEGORY = "TenserTensor/Workflow"


@dataclass
class TTWorkflowSettings():
    ascore_negative: float | None = None
    ascore_positive: float | None = None
    cfg: int | None = None
    clip_g_negative: str | None = None
    clip_l_negative: str | None = None
    clip_g_positive: str | None = None
    clip_l_positive: str | None = None
    guidance: float | None = None
    height: int | None = None
    lora_triggers: str | None = None
    prompt: str | None = None
    sampler: Sampler | None = None
    sampler_name: str | None = None
    scheduler: str | None = None
    seed: int | None = None
    sigmas: torch.Tensor | None = None
    steps: int | None = None
    target_height: int | None = None
    target_width: int | None = None
    t5xxl_negative: str | None = None
    t5xxl_positive: str | None = None
    width: int | None = None

    @classmethod
    def create(cls, **kwargs) -> TTWorkflowSettings:
        wf = cls()
        for field in dataclasses.fields(wf):
            wf.set_attr(field.name, kwargs.get(field.name, None))

        return wf

    def update_attrs(self, **kwargs) -> TTWorkflowSettings:
        for key in kwargs.keys():
            if hasattr(self, key):
                val = kwargs.get(key)
                if val is not None:
                    self.set_attr(key, val)

        return self

    def set_attr(self, key, attr) -> None:
        if hasattr(self, key):
            setattr(self, key, attr)

    def get_attr(self, key, default=None) -> None:
        if hasattr(self, key):
            val = getattr(self, key)
            return val if val is not None else default


@io.comfytype(io_type="TT_WORKFLOW_CONFIG")
class WorkflowSettings:
    Type = TTWorkflowSettings

    class Input(io.Input):
        def __init__(self, id: str, **kwargs):
            super().__init__(id, **kwargs)

    class Output(io.Output):
        def __init__(self, **kwargs):
            print()
            super().__init__(**kwargs)


class TT_SdxlWorkflowSettingsNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_SdxlWorkflowSettingsNode",
            display_name="TT SDXL Workflow Settings",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Combo.Input("scheduler", options=KSampler.SCHEDULERS),
                io.Float.Input("ascore_positive", default=9.0, min=0.0, max=100.0, step=0.1),
                io.Float.Input("ascore_negative", default=6.0, min=0.0, max=100.0, step=0.1),
                io.Int.Input("width", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_width", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Int.Input("target_height", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.String.Output("SAMPLER_NAME"),
                io.String.Output("SCHEDULER"),
                io.Float.Output("ASCORE_POSITIVE"),
                io.Float.Output("ASCORE_NEGATIVE"),
                io.Int.Output("WIDTH"),
                io.Int.Output("HEIGHT"),
                io.Int.Output("TARGET_WIDTH"),
                io.Int.Output("TARGET_HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {"workflow_config": workflow_config, **kwargs}

        return io.NodeOutput(*args.values())


class TT_SdxlWorkflowSettingsAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_SdxlWorkflowSettingsAdvancedNode",
            display_name="TT SDXL Workflow Settings (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Combo.Input("scheduler", options=KSampler.SCHEDULERS),
                io.Float.Input("ascore_positive", default=9.0, min=0.0, max=100.0, step=0.1),
                io.Float.Input("ascore_negative", default=6.0, min=0.0, max=100.0, step=0.1),
                io.String.Input("clip_l_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_g_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_l_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_g_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("lora_triggers", multiline=True, dynamic_prompts=True, advanced=True),
                io.Int.Input("width", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_width", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Int.Input("target_height", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.String.Output("SAMPLER_NAME"),
                io.String.Output("SCHEDULER"),
                io.Float.Output("ASCORE_POSITIVE"),
                io.Float.Output("ASCORE_NEGATIVE"),
                io.String.Output("CLIP_L_POSITIVE"),
                io.String.Output("CLIP_G_POSITIVE"),
                io.String.Output("CLIP_L_NEGATIVE"),
                io.String.Output("CLIP_G_NEGATIVE"),
                io.String.Output("LORA_TRIGGERS"),
                io.Int.Output("WIDTH"),
                io.Int.Output("HEIGHT"),
                io.Int.Output("TARGET_WIDTH"),
                io.Int.Output("TARGET_HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {"workflow_config": workflow_config, **kwargs}

        return io.NodeOutput(*args.values())


class TT_FluxWorkflowSettingsNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_FluxWorkflowSettingsNode",
            display_name="TT FLUX Workflow Settings",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Combo.Input("scheduler", options=KSampler.SCHEDULERS),
                io.Float.Input("guidance", default=3.0, min=1.0, max=10.0, step=0.1),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.String.Output("SAMPLER_NAME"),
                io.String.Output("SCHEDULER"),
                io.Float.Output("GUIDANCE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {"workflow_config": workflow_config, **kwargs}

        return io.NodeOutput(*args.values())


class TT_FluxWorkflowSettingsAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_FluxWorkflowSettingsAdvancedNode",
            display_name="TT FLUX Workflow Settings (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Combo.Input("scheduler", options=KSampler.SCHEDULERS),
                io.String.Input("clip_l_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("t5xxl_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_l_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("t5xxl_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("lora_triggers", multiline=True, dynamic_prompts=True, advanced=True),
                io.Float.Input("guidance", default=3.0, min=1.0, max=10.0, step=0.1),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.String.Output("SAMPLER_NAME"),
                io.String.Output("SCHEDULER"),
                io.String.Output("CLIP_L_POSITIVE"),
                io.String.Output("T5XXL_POSITIVE"),
                io.String.Output("CLIP_L_NEGATIVE"),
                io.String.Output("T5XXL_NEGATIVE"),
                io.String.Output("LORA_TRIGGERS"),
                io.Float.Output("GUIDANCE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {"workflow_config": workflow_config, **kwargs}

        return io.NodeOutput(*args.values())


def compute_empirical_mu(image_seq_len, num_steps):
    slope_high_res, intercept_high_res = 8.73809524e-05, 1.89833333
    slope_low_res, intercept_low_res = 0.00016927, 0.45666666
    HIGH_RES_THRESHOLD = 4300
    MIN_STEPS, MAX_STEPS = 10, 200
    mu_at_max_steps = slope_low_res * image_seq_len + intercept_low_res

    if image_seq_len > HIGH_RES_THRESHOLD:
        return float(mu_at_max_steps)

    mu_at_min_steps = slope_high_res * image_seq_len + intercept_high_res
    slope = (mu_at_max_steps - mu_at_min_steps) / (MAX_STEPS - MIN_STEPS)
    intercept = mu_at_max_steps - MAX_STEPS * slope
    mu = slope * num_steps + intercept

    return float(mu)


def generalized_time_snr_shift(t, mu, sigma):
    return math.exp(mu) / (math.exp(mu) + (1 / t - 1) ** sigma)


def get_schedule(steps, width, height):
    image_seq_len = (width * height / (16 * 16))
    mu = compute_empirical_mu(image_seq_len, steps)
    timesteps = torch.linspace(1, 0, steps + 1)
    timesteps = generalized_time_snr_shift(timesteps, mu, 1.0)

    return timesteps


def build_sampler_sigmas(sampler_name, steps, width, height):
    sampler = sampler_object(sampler_name)
    sigmas = get_schedule(steps, width, height)

    return sampler, sigmas


class TT_Flux2WorkflowSettingsNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux2WorkflowSettingsNode",
            display_name="TT FLUX2 Workflow Settings",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.Float.Input("guidance", default=3.0, min=1.0, max=10.0, step=0.1),
                io.Int.Input("width", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS)
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Sampler.Output("SAMPLER"),
                io.Sigmas.Output("SIGMAS"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.Float.Output("GUIDANCE"),
                io.Int.Output("WIDTH"),
                io.Int.Output("HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["sampler"], kwargs["sigmas"] = build_sampler_sigmas(
            kwargs.get("sampler_name"),
            kwargs.get("steps"),
            kwargs.get("width"),
            kwargs.get("height"),
        )

        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {
            "workflow_config": workflow_config,
            "sampler": kwargs["sampler"],
            "sigmas": kwargs["sigmas"],
            "seed": kwargs.get("seed"),
            "steps": kwargs.get("steps"),
            "cfg": kwargs.get("cfg"),
            "guidance": kwargs.get("guidance"),
            "width": kwargs.get("width"),
            "height": kwargs.get("height"),
        }

        return io.NodeOutput(*args.values())


class TT_Flux2WorkflowSettingsAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux2WorkflowSettingsAdvancedNode",
            display_name="TT FLUX2 Workflow Settings (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Int.Input("width", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.String.Input("prompt", multiline=True, dynamic_prompts=True),
                io.String.Input("lora_triggers", multiline=True, dynamic_prompts=True),
                io.Float.Input("guidance", default=3.0, min=1.0, max=10.0, step=0.1),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Sampler.Output("SAMPLER"),
                io.Sigmas.Output("SIGMAS"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.Int.Output("WIDTH"),
                io.Int.Output("HEIGHT"),
                io.String.Output("PROMPT"),
                io.String.Output("LORA_TRIGGERS"),
                io.Float.Output("GUIDANCE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["sampler"], kwargs["sigmas"] = build_sampler_sigmas(
            kwargs.get("sampler_name"), kwargs.get("steps"), kwargs.get("width"), kwargs.get("height"),
        )

        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {
            "workflow_config": workflow_config,
            "sampler": kwargs["sampler"],
            "sigmas": kwargs["sigmas"],
            "seed": kwargs.get("seed"),
            "steps": kwargs.get("steps"),
            "cfg": kwargs.get("cfg"),
            "width": kwargs.get("width"),
            "height": kwargs.get("height"),
            "prompt": kwargs.get("prompt"),
            "lora_triggers": kwargs.get("lora_triggers"),
            "guidance": kwargs.get("guidance"),
        }

        return io.NodeOutput(*args.values())


def sd3_shift_sigma(sigma, schedule_shift):
    return schedule_shift * sigma / (1 + (schedule_shift - 1) * sigma)


def build_sd3_sampler_sigmas(sampler_name, steps, schedule_shift=3.0):
    sampler = sampler_object(sampler_name)
    timesteps = torch.linspace(1, 0, steps + 1)
    sigmas = sd3_shift_sigma(timesteps, schedule_shift)

    return sampler, sigmas


class TT_Sd35GgufWorkflowSettingsNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Sd35GgufWorkflowSettingsNode",
            display_name="TT SD3.5 GGUF Workflow Settings",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Float.Input("schedule_shift", default=3.0, min=0.0, max=20.0, step=0.1, advanced=True),
                io.Int.Input("width", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_width", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Int.Input("target_height", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Sampler.Output("SAMPLER"),
                io.Sigmas.Output("SIGMAS"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.Int.Output("WIDTH"),
                io.Int.Output("HEIGHT"),
                io.Int.Output("TARGET_WIDTH"),
                io.Int.Output("TARGET_HEIGHT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["sampler"], kwargs["sigmas"] = build_sd3_sampler_sigmas(
            kwargs.get("sampler_name"), kwargs.get("steps"), kwargs.get("schedule_shift"),
        )

        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {
            "workflow_config": workflow_config,
            "sampler": kwargs["sampler"],
            "sigmas": kwargs["sigmas"],
            "seed": kwargs.get("seed"),
            "steps": kwargs.get("steps"),
            "cfg": kwargs.get("cfg"),
            "width": kwargs.get("width"),
            "height": kwargs.get("height"),
            "target_width": kwargs.get("target_width"),
            "target_height": kwargs.get("target_height"),
        }

        return io.NodeOutput(*args.values())


class TT_Sd35GgufWorkflowSettingsAdvancedNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Sd35GgufWorkflowSettingsAdvancedNode",
            display_name="TT SD3.5 GGUF Workflow Settings (Advanced)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.Float.Input("schedule_shift", default=3.0, min=0.0, max=20.0, step=0.1, advanced=True),
                io.String.Input("clip_l_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_g_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("t5xxl_positive", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_l_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("clip_g_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("t5xxl_negative", multiline=True, dynamic_prompts=True),
                io.String.Input("lora_triggers", multiline=True, dynamic_prompts=True, advanced=True),
                io.Int.Input("width", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=1024, min=16, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_width", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
                io.Int.Input("target_height", default=1024, min=16, max=MAX_RESOLUTION, step=8, advanced=True),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Sampler.Output("SAMPLER"),
                io.Sigmas.Output("SIGMAS"),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.Int.Output("WIDTH"),
                io.Int.Output("HEIGHT"),
                io.Int.Output("TARGET_WIDTH"),
                io.Int.Output("TARGET_HEIGHT"),
                io.String.Output("CLIP_L_POSITIVE"),
                io.String.Output("CLIP_G_POSITIVE"),
                io.String.Output("T5XXL_POSITIVE"),
                io.String.Output("CLIP_L_NEGATIVE"),
                io.String.Output("CLIP_G_NEGATIVE"),
                io.String.Output("T5XXL_NEGATIVE"),
                io.String.Output("LORA_TRIGGERS"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        kwargs["sampler"], kwargs["sigmas"] = build_sd3_sampler_sigmas(
            kwargs.get("sampler_name"), kwargs.get("steps"), kwargs.get("schedule_shift"),
        )

        workflow_config = TTWorkflowSettings.create(**kwargs)
        args = {
            "workflow_config": workflow_config,
            "sampler": kwargs["sampler"],
            "sigmas": kwargs["sigmas"],
            "seed": kwargs.get("seed"),
            "steps": kwargs.get("steps"),
            "cfg": kwargs.get("cfg"),
            "width": kwargs.get("width"),
            "height": kwargs.get("height"),
            "target_width": kwargs.get("target_width"),
            "target_height": kwargs.get("target_height"),
            "clip_l_positive": kwargs.get("clip_l_positive"),
            "clip_g_positive": kwargs.get("clip_g_positive"),
            "t5xxl_positive": kwargs.get("t5xxl_positive"),
            "clip_l_negative": kwargs.get("clip_l_negative"),
            "clip_g_negative": kwargs.get("clip_g_negative"),
            "t5xxl_negative": kwargs.get("t5xxl_negative"),
            "lora_triggers": kwargs.get("lora_triggers"),
        }

        return io.NodeOutput(*args.values())


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

class WorkflowNodesExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            TT_SdxlWorkflowSettingsNode,
            TT_SdxlWorkflowSettingsAdvancedNode,
            TT_FluxWorkflowSettingsNode,
            TT_FluxWorkflowSettingsAdvancedNode,
            TT_Flux2WorkflowSettingsNode,
            TT_Flux2WorkflowSettingsAdvancedNode,
            TT_Sd35GgufWorkflowSettingsNode,
            TT_Sd35GgufWorkflowSettingsAdvancedNode,
        ]


async def comfy_entrypoint() -> WorkflowNodesExtension:
    return WorkflowNodesExtension()


# ==============================================================================
# Re-exports for backward compatibility
# ==============================================================================

__all__ = [
    "TT_SdxlWorkflowSettingsNode",
    "TT_SdxlWorkflowSettingsAdvancedNode",
    "TT_FluxWorkflowSettingsNode",
    "TT_FluxWorkflowSettingsAdvancedNode",
    "TT_Flux2WorkflowSettingsNode",
    "TT_Flux2WorkflowSettingsAdvancedNode",
    "TT_Sd35GgufWorkflowSettingsNode",
    "TT_Sd35GgufWorkflowSettingsAdvancedNode",
]
