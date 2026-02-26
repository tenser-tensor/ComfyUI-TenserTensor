# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .context_helpers import create_context_schema


class TT_ContextSetLatent:
    INPUT_TYPES_DICT, RETURN_TYPES, RETURN_NAMES = create_context_schema("set_latent")
    FUNCTION = "process_context"
    CATEGORY = "TenserTensor/Deprecated/Context"

    @classmethod
    def INPUT_TYPES(cls):
        return cls.INPUT_TYPES_DICT

    def process_context(self, context, latent):
        context["latent"] = latent

        return (context,)
