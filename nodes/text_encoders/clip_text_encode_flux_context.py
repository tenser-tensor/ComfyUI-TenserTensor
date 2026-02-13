from .encoder_helpers import encode_prompts_flux


class TT_ClipTextEncodeFluxContext():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context": ("TT_CONTEXT",)
            }
        }

    RETURN_TYPES = ("TT_CONTEXT", "CONDITIONING", "CONDITIONING",)
    RETURN_NAMES = ("CONTEXT", "POSITIVE", "NEGATIVE",)
    FUNCTION = "execute"
    CATEGORY = "TenserTensor/Text Encoders/FLUX"

    def execute(self, context):
        clip = context["clip"]
        config = context["workflow_config"]

        positive, negative = encode_prompts_flux(
            clip,
            config["clip_l_positive"],
            config["t5xxl_positive"],
            config["clip_l_negative"],
            config["t5xxl_negative"],
            config["guidance"],
        )

        context["positive"] = positive
        context["negative"] = negative

        return (context, positive, negative,)
