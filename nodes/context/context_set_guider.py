# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .context_helpers import create_context_schema


class TT_ContextSetGuider:
    INPUT_TYPES_DICT, RETURN_TYPES, RETURN_NAMES = create_context_schema("set_guider")
    FUNCTION = "process_context"
    CATEGORY = "TenserTensor/Context"

    @classmethod
    def INPUT_TYPES(cls):
        return cls.INPUT_TYPES_DICT

    def process_context(self, context, guider):
        context["guider"] = guider

        return (context,)
