# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.samplers

from .ksampler_helpers import sample_latents


class TT_KSamplerTwoStage():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent": ("LATENT",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "cfg": ("FLOAT", {"default": 1.5, "min": 0.0, "max": 100.0, "step": 0.1}),
                "draft_steps": ("INT", {"default": 25, "min": 1, "max": 10000}),
                "refiner_steps": ("INT", {"default": 25, "min": 1, "max": 10000}),
                "draft_sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "draft_scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "refiner_sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "refiner_scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "draft_denoise": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "refiner_denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)
    FUNCTION = "execute_sampling"
    CATEGORY = "TenserTensor/Sampling"

    def execute_sampling(self, **kwargs):
        draft_steps = kwargs["draft_steps"]
        refiner_steps = kwargs["refiner_steps"]

        args = {
            "model": kwargs["model"],
            "positive": kwargs["positive"],
            "negative": kwargs["negative"],
            "latent": kwargs["latent"],
            "seed": kwargs["seed"],
            "steps": draft_steps,
            "start_step": 0,
            "cfg": kwargs["cfg"],
            "sampler_name": kwargs["draft_sampler_name"],
            "scheduler": kwargs["draft_scheduler"],
            "add_noise": True,
            "full_denoise": False,
            "denoise": kwargs["refiner_denoise"],
        }

        samples = sample_latents(**args)

        args["latent"] = samples
        args["steps"] = draft_steps + refiner_steps
        args["start_step"] = draft_steps
        args["denoise"] = kwargs["draft_denoise"]
        args["sampler_name"] = kwargs["refiner_sampler_name"]
        args["scheduler"] = kwargs["refiner_scheduler"]
        args["full_denoise"] = True

        return (sample_latents(**args),)
