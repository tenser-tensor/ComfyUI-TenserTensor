# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .context_helpers import (build_return_tuple, create_context_schema, init_context)


class TT_EvenLargerContext:
    INPUT_TYPES_DICT, RETURN_TYPES, RETURN_NAMES = create_context_schema("huge")
    FUNCTION = "process_context"
    CATEGORY = "TenserTensor/Context"

    @classmethod
    def INPUT_TYPES(cls):
        return cls.INPUT_TYPES_DICT

    def process_context(self, context=None, **kwargs):
        args = init_context(context, **kwargs)

        return build_return_tuple("huge", args)
