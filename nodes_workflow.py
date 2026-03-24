# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)
import math

import torch

from comfy.samplers import KSampler, sampler_object
from comfy_api.latest import io
from .nodes_workflow_d import WorkflowSettings, TTWorkflowSettings
from .utils import CommonTypes

CATEGORY = "TenserTensor/Workflow"


# ==============================================================================
# Helper functions — pipeline utilities and loaders
# ==============================================================================

def ltxv_sigmas(**kwargs):
    latent, scheduler_config = (
        kwargs.get("video_latent_opt"),
        kwargs.get("scheduler_config"),
    )

    base_shift, max_shift = 0.95, 2.05
    if scheduler_config.get("scheduler_config") == "Manual":
        base_shift = scheduler_config.get("schedule_base_shift", 0.95),
        max_shift = scheduler_config.get("schedule_max_shift", 2.05)

    token_count = math.prod(latent["samples"].shape[2:]) if latent else 4096
    sigmas = torch.linspace(1.0, 0.0, kwargs.get("steps") + 1)

    MIN_STEPS, MAX_STEPS = 1024, 4096

    slope = (max_shift - base_shift) / (MAX_STEPS - MIN_STEPS)
    intercept = base_shift - slope * MIN_STEPS
    sigma_shift = (token_count) * slope + intercept
    sigma = 1.0
    timesteps = math.exp(sigma_shift) / (math.exp(sigma_shift) + (1 / sigmas - 1) ** sigma)
    sigmas = torch.where(sigmas != 0, timesteps, 0)

    stretch_sigmas = kwargs.get("stretch_sigmas")
    if stretch_sigmas.get("stretch_sigmas") == "In Range":
        non_zero_mask = sigmas != 0
        non_zero_sigmas = sigmas[non_zero_mask]
        one_minus_z = 1.0 - non_zero_sigmas
        scale_factor = one_minus_z[-1] / (1.0 - stretch_sigmas.get("sigmas_terminal", 0.1))
        stretched = 1.0 - (one_minus_z / scale_factor)
        sigmas[non_zero_mask] = stretched

    return sigmas


def build_ltxv_sampler_sigmas(**kwargs):
    sampler = sampler_object(kwargs.get("sampler_name"))
    sigmas = ltxv_sigmas(**kwargs)

    return sampler, sigmas


# ==============================================================================
# Node classes — ComfyUI node definitions
# ==============================================================================


class TT_LtxvWorkflowSettingsNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LtxvWorkflowSettingsNode",
            display_name="TT LTXV Workflow Settings",
            category=CATEGORY,
            description="",
            inputs=[
                io.Latent.Input("video_latent_opt", optional=True),
                io.Combo.Input("sampler_name", options=KSampler.SAMPLERS),
                io.DynamicCombo.Input("stretch_sigmas", options=[
                    io.DynamicCombo.Option("In Range", [
                        io.Float.Input("sigmas_terminal", default=0.1, min=0.0, max=0.99, step=0.01),
                    ]),
                    io.DynamicCombo.Option("Bypass", []),
                ]),
                io.DynamicCombo.Input("scheduler_config", options=[
                    io.DynamicCombo.Option("Defaults", []),
                    io.DynamicCombo.Option("Manual", [
                        io.Float.Input("schedule_base_shift", default=0.95, min=0.0, max=10.0, step=0.01),
                        io.Float.Input("schedule_max_shift", default=2.05, min=0.0, max=10.0, step=0.01),
                    ]),
                ]),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Int.Input("noise_seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Int.Input("steps", default=30, min=1, max=10_000),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.Float.Input("length_sec", default=5.0, min=0.1, max=120.0, step=0.1),
                io.Combo.Input("frame_rate", options=CommonTypes.FRAME_RATES, default="24fps"),
            ],
            outputs=[
                WorkflowSettings.Output("WORKFLOW_CONFIG"),
                io.Sampler.Output("SAMPLER"),
                io.Sigmas.Output("SIGMAS"),
                io.Int.Output("SEED"),
                io.Int.Output("NOISE_SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.String.Output("LENGTH_SEC"),
                io.String.Output("FRAME_RATE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        workflow_config = TTWorkflowSettings.create(**kwargs)

        sampler, sigmas = build_ltxv_sampler_sigmas(**kwargs)
        workflow_config.set_attr("sampler", sampler)
        workflow_config.set_attr("sigmas", sigmas)

        args = (
            workflow_config,
            sampler,
            sigmas,
            kwargs.get("seed"),
            kwargs.get("noise_seed"),
            kwargs.get("steps"),
            kwargs.get("cfg"),
            kwargs.get("length_sec"),
            kwargs.get("frame_rate"),
        )

        return io.NodeOutput(workflow_config, *args)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

NODES = [
    TT_LtxvWorkflowSettingsNode,
]
