# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.samplers

import nodes


class TT_SdxlWorkflowSettingsAdvanced:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 30, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "clip_l_positive": (
                    "STRING",
                    {"multiline": True, "placeholder": "CLIP_L Positive", "dynamicPrompts": True}
                ),
                "clip_g_positive": (
                    "STRING",
                    {"multiline": True, "placeholder": "CLIP_G Positive", "dynamicPrompts": True}
                ),
                "clip_l_negative": (
                    "STRING",
                    {"multiline": True, "placeholder": "CLIP_L Negative", "dynamicPrompts": True}
                ),
                "clip_g_negative": (
                    "STRING",
                    {"multiline": True, "placeholder": "CLIP_G Negative", "dynamicPrompts": True}
                ),
                "ascore_positive": ("FLOAT", {"default": 9.0, "min": 0.0, "max": 1000.0, "step": 0.1}),
                "ascore_negative": ("FLOAT", {"default": 6.0, "min": 0.0, "max": 1000.0, "step": 0.1}),
                "width": ("INT", {"default": 512, "min": 0.0, "max": nodes.MAX_RESOLUTION}),
                "height": ("INT", {"default": 512, "min": 0.0, "max": nodes.MAX_RESOLUTION}),
                "target_width": ("INT", {"default": 512, "min": 0.0, "max": nodes.MAX_RESOLUTION}),
                "target_height": ("INT", {"default": 512, "min": 0.0, "max": nodes.MAX_RESOLUTION}),
            }
        }

    RETURN_TYPES = (
        "TT_WORKFLOW_CONFIG",
        "INT",
        "INT",
        "FLOAT",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "FLOAT",
        "FLOAT",
        "INT",
        "INT",
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "WORKFLOW_CONFIG",
        "SEED",
        "STEPS",
        "CFG",
        "SAMPLER_NAME",
        "SCHEDULER",
        "CLIP_L_POSITIVE",
        "CLIP_G_POSITIVE",
        "CLIP_L_NEGATIVE",
        "CLIP_G_NEGATIVE",
        "ASCORE_POSITIVE",
        "ASCORE_NEGATIVE",
        "WIDTH",
        "HEIGHT",
        "TARGET_WIDTH",
        "TARGET_HEIGHT",
    )
    FUNCTION = "get_settings"
    CATEGORY = "TenserTensor/Workflow/SDXL"

    def get_settings(self, seed, steps, cfg, sampler_name, scheduler, clip_l_positive, clip_g_positive, clip_l_negative,
                     clip_g_negative, ascore_positive, ascore_negative, width, height, target_width, target_height):
        workflow_config = {
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "clip_l_positive": clip_l_positive,
            "clip_g_positive": clip_g_positive,
            "clip_l_negative": clip_l_negative,
            "clip_g_negative": clip_g_negative,
            "ascore_positive": ascore_positive,
            "ascore_negative": ascore_negative,
            "width": width,
            "height": height,
            "target_width": target_width,
            "target_height": target_height,
        }

        return (workflow_config, seed, steps, cfg, sampler_name, scheduler, clip_l_positive, clip_g_positive,
                clip_l_negative,
                clip_g_negative, ascore_positive, ascore_negative, width, height, target_width, target_height)
