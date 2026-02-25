# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.samplers

from .ksampler_helpers import sample_latents


class TT_KSamplerAdvanced():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent": ("LATENT",),
                "add_noise": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "full_denoise": ("BOOLEAN", {"default": False, "label_on": "Enabled", "label_off": "Disabled"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 10000}),
                "start_step": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "last_step": ("INT", {"default": 10000, "min": 0, "max": 10000}),
                "cfg": ("FLOAT", {"default": 1.5, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("SAMPLES",)
    FUNCTION = "execute_sampling"
    CATEGORY = "TenserTensor/Sampling"

    def execute_sampling(self, **kwargs):
        return (sample_latents(**kwargs),)
