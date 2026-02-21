# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .ksampler_helpers import guided_sample_latents


class TT_KSamplerGuided:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "guider": ("GUIDER",),
                "sigmas": ("SIGMAS",),
                "sampler": ("SAMPLER",),
                "random_noise": ("NOISE",),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("SAMPLES",)
    FUNCTION = "execute_sampling"
    CATEGORY = "TenserTensor/Sampling"

    def execute_sampling(self, latent, guider, sigmas, sampler, random_noise):
        return (guided_sample_latents(latent, guider, sigmas, sampler, random_noise),)
