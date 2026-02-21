# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.samplers as S


class TT_FluxWorkflowSettingsAdvanced:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 1.5, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sampler_name": (S.KSampler.SAMPLERS,),
                "scheduler": (S.KSampler.SCHEDULERS,),
                "clip_l_positive": ("STRING", {"multiline": True, "placeholder": "CLIP_L Positive", "dynamicPrompts": True}),
                "t5xxl_positive": ("STRING", {"multiline": True, "placeholder": "T5XXL Positive", "dynamicPrompts": True}),
                "clip_l_negative": ("STRING", {"multiline": True, "placeholder": "CLIP_L Negative", "dynamicPrompts": True}),
                "t5xxl_negative": ("STRING", {"multiline": True, "placeholder": "CLIP_L Negative", "dynamicPrompts": True}),
                "guidance": ("FLOAT", {"default": 3.5, "min": 1.0, "max": 10.0, "step": 0.1})
            }
        }

    RETURN_TYPES = (
        "TT_WORKFLOW_CONFIG",
        "INT",
        "INT",
        "FLOAT",
        S.KSampler.SAMPLERS,
        S.KSampler.SCHEDULERS,
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "FLOAT",
    )
    RETURN_NAMES = (
        "WORKFLOW_CONFIG",
        "SEED",
        "STEPS",
        "CFG",
        "SAMPLER_NAME",
        "SCHEDULER",
        "CLIP_L_POSITIVE",
        "T5XXL_POSITIVE",
        "CLIP_L_NEGATIVE",
        "T5XXL_NEGATIVE",
        "GUIDANCE",
    )
    FUNCTION = "get_settings"
    CATEGORY = "TenserTensor/Workflow/FLUX"

    def get_settings(self, seed, steps, cfg, sampler_name, scheduler, guidance, clip_l_positive, t5xxl_positive, clip_l_negative, t5xxl_negative):
        workflow_config = {
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "clip_l_positive": clip_l_positive,
            "t5xxl_positive": t5xxl_positive,
            "clip_l_negative": clip_l_negative,
            "t5xxl_negative": t5xxl_negative,
            "guidance": guidance
        }

        return (workflow_config, seed, steps, cfg, sampler_name, scheduler, guidance, clip_l_positive, t5xxl_positive, clip_l_negative,
                t5xxl_negative)
