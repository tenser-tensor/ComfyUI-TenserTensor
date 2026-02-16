from .context_helpers import create_context_schema


class TT_ContextSetImage:
    INPUT_TYPES_DICT, RETURN_TYPES, RETURN_NAMES = create_context_schema("set_image")
    FUNCTION = "process_context"
    CATEGORY = "TenserTensor/Context"

    @classmethod
    def INPUT_TYPES(cls):
        return cls.INPUT_TYPES_DICT

    def process_context(self, context, image):
        context["image"] = image

        return (context,)
