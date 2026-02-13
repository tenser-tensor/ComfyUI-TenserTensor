from .ksampler_helpers import sample_latents


class TT_KSamplerContext():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context": ("TT_CONTEXT",)
            }
        }

    RETURN_TYPES = ("TT_CONTEXT", "LATENT",)
    RETURN_NAMES = ("CONTEXT", "LATENT",)
    FUNCTION = "execute_sampling"
    CATEGORY = "TenserTensor/Sampling"

    def execute_sampling(self, context):
        model = context.get("model", None)
        latent = context.get("latent", None)
        config = context.get("workflow_config", None)

        if model is None:
            raise ValueError("Model is required for sampling")
        if latent is None:
            raise ValueError("Latent image is required for sampling")
        if config is None:
            raise ValueError("Workflow Config is required for sampling")

        args = {
            "model": model,
            "positive": context.get("positive", None),
            "negative": context.get("negative", None),
            "latent": latent,
            "seed": config.get("seed", 0),
            "steps": config.get("steps", 0),
            "cfg": config.get("cfg", 0),
            "sampler_name": config.get("sampler_name", None),
            "scheduler": config.get("scheduler", None),
        }

        samples = sample_latents(**args)

        return (context, samples)
