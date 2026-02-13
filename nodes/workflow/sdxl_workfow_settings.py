import comfy.samplers


class TT_SdxlWorkflowSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 30, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
            }
        }

    RETURN_TYPES = (
        "TT_WORKFLOW_CONFIG",
        "INT",
        "INT",
        "FLOAT",
        comfy.samplers.KSampler.SAMPLERS,
        comfy.samplers.KSampler.SCHEDULERS,
    )

    RETURN_NAMES = (
        "WORKFLOW_CONFIG",
        "SEED",
        "STEPS",
        "CFG",
        "SAMPLER_NAME",
        "SCHEDULER",
    )

    FUNCTION = "get_settings"
    CATEGORY = "TenserTensor/Workflow/SDXL"

    def get_settings(self, seed, steps, cfg, sampler_name, scheduler):
        workflow_config = {
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
        }

        return (workflow_config, seed, steps, cfg, sampler_name, scheduler)
