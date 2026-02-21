# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.samplers as S

from nodes import MAX_RESOLUTION
from .workflow_settings_helpers import get_schedule


class TT_Flux2WorkflowSettingsAdvanced:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sampler_name": (S.KSampler.SAMPLERS,),
                "width": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                "prompt": ("STRING", {"multiline": True, "placeholder": "Prompt", "dynamicPrompts": True}),
                "lora_triggers": ("STRING", {"multiline": True, "placeholder": "LoRA Triggers", "dynamicPrompts": True}),
                "guidance": ("FLOAT", {"default": 3.5, "min": 1.0, "max": 10.0, "step": 0.1})
            }
        }

    RETURN_TYPES = (
        "TT_WORKFLOW_CONFIG",
        "INT",
        "INT",
        "FLOAT",
        "SAMPLER",
        S.KSampler.SAMPLERS,
        "SIGMAS",
        "INT",
        "INT",
        "FLOAT"
    )
    RETURN_NAMES = (
        "WORKFLOW_CONFIG",
        "SEED",
        "STEPS",
        "CFG",
        "SAMPLER",
        "SAMPLER_NAME",
        "SCHEDULER",
        "WIDTH",
        "HEIGHT",
        "PROMPT",
        "GUIDANCE"
    )
    FUNCTION = "get_settings"
    CATEGORY = "TenserTensor/Workflow/FLUX2"

    def get_settings(self, seed, steps, cfg, sampler_name, width, height, prompt, lora_triggers, guidance):
        scheduler = get_schedule(seed, width, height)
        sampler = S.sampler_object(sampler_name)

        workflow_config = {
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler": sampler,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "width": width,
            "height": height,
            "prompt": prompt,
            "lora_triggers": lora_triggers,
            "guidance": guidance
        }

        return (workflow_config, seed, steps, cfg, sampler, scheduler, width, height, prompt, lora_triggers, guidance)
