from .context_helpers import (build_return_tuple, create_context_schema, init_context)


class TT_LargeContextFlux:
    INPUT_TYPES_DICT, RETURN_TYPES, RETURN_NAMES = create_context_schema("big_flux")
    FUNCTION = "process_context"
    CATEGORY = "TenserTensor/Context"

    @classmethod
    def INPUT_TYPES(cls):
        return cls.INPUT_TYPES_DICT

    def process_context(self, context=None, **kwargs):
        args = init_context(context, **kwargs)

        return build_return_tuple("big_flux", args)
