import comfy.samplers

CONTEXT_FIELDS = [
    # input_name, return_name, field_type
    ("context", "CONTEXT", "TT_CONTEXT",),
    ("model", "MODEL", "MODEL",),
    ("clip", "CLIP", "CLIP",),
    ("vae", "VAE", "VAE",),
    ("latent", "LATENT", "LATENT",),
    ("positive", "POSITIVE", "CONDITIONING"),
    ("negative", "NEGATIVE", "CONDITIONING"),
    ("image", "IMAGE", "IMAGE"),
    ("mask", "MASK", "MASK"),
    ("control_net", "CONTROL_NET", "CONTROL_NET"),
    ("workflow_config", "WORKFLOW_CONFIG", "TT_WORKFLOW_CONFIG",),
    ("seed", "SEED", "INT"),
    ("steps", "STEPS", "INT"),
    ("cfg", "CFG", "FLOAT"),
    ("sampler_name", "SAMPLER_NAME", comfy.samplers.KSampler.SAMPLERS),
    ("scheduler", "SCHEDULER", comfy.samplers.KSampler.SCHEDULERS),
    ("guidance", "GUIDANCE", "FLOAT"),
    ("clip_l_positive", "CLIP_L_POSITIVE", "STRING"),
    ("clip_g_positive", "CLIP_L_POSITIVE", "STRING"),
    ("t5xxl_positive", "T5XXL_POSITIVE", "STRING"),
    ("clip_l_negative", "CLIP_L_NEGATIVE", "STRING"),
    ("clip_g_negative", "CLIP_L_NEGATIVE", "STRING"),
    ("t5xxl_negative", "T5XXL_NEGATIVE", "STRING"),
    ("ascore_positive", "ASCORE_POSITIVE", "FLOAT"),
    ("ascore_negative", "ASCORE_NEGATIVE", "FLOAT"),
    ("width", "WIDTH", "INT"),
    ("height", "HEIGHT", "INT"),
    ("target_width", "TARGET_WIDTH", "INT"),
    ("target_height", "TARGET_HEIGHT", "INT"),
]

CONTEXTS = {
    "base": {
        "required": (
            "model",
            "clip",
            "vae",
            "latent",
        ),
        "optional": (
            "workflow_config",
        ),
        "return": (
            "context",
        )
    },
    "standard": {
        "optional": (
            "context",
            "workflow_config",
            "model",
            "clip",
            "vae",
            "positive",
            "negative",
            "latent",
            "image",
            "seed",
            "steps",
            "cfg",
            "sampler_name",
            "scheduler",
        )
    },
    "big_flux": {
        "optional": (
            "context",
            "workflow_config",
            "model",
            "clip",
            "vae",
            "positive",
            "negative",
            "latent",
            "image",
            "seed",
            "steps",
            "cfg",
            "sampler_name",
            "scheduler",
            "guidance",
            "clip_l_positive",
            "t5xxl_positive",
            "clip_l_negative",
            "t5xxl_negative",
            "width",
            "height",
        )
    },
    "big_sdxl": {
        "optional": (
            "context",
            "workflow_config",
            "model",
            "clip",
            "vae",
            "positive",
            "negative",
            "latent",
            "image",
            "seed",
            "steps",
            "cfg",
            "sampler_name",
            "scheduler",
            "guidance",
            "clip_l_positive",
            "clip_g_positive",
            "clip_l_negative",
            "clip_g_negative",
            "ascore_positive",
            "ascore_negative",
            "width",
            "height",
            "target_width",
            "target_height",
        )
    },
    "huge": {
        "optional": tuple(f[0] for f in CONTEXT_FIELDS)
    },
    "passthrough": {
        "required": (
            "context",
        )
    },
}

FORCE_INPUT_TYPES = {
    "INT",
    "FLOAT",
    "STRING",
    "BOOLEAN",
}

WORKFOW_SETTINGS_KEYS = [
    "seed",
    "steps",
    "cfg",
    "sampler_name",
    "scheduler",
    "pos_a_score",
    "clip_l_positive",
    "clip_g_positive",
    "t5xxl_positive",
    "neg_a_score",
    "clip_l_negative",
    "clip_g_negative",
    "t5xxl_negative",
    "guidance",
    "ascore_positive",
    "ascore_negative",
    "width",
    "height",
    "target_width",
    "target_height",
]


def _get_field_map():
    return {field[0]: (field[1], field[2]) for field in CONTEXT_FIELDS}


def _get_input_types(field_map, fields):
    retval = {}
    for field_name in fields:
        field_type = field_map[field_name][1]

        if isinstance(field_type, (list, tuple)) or field_type in FORCE_INPUT_TYPES:
            retval[field_name] = (field_type, {"forceInput": True})
        else:
            retval[field_name] = (field_type,)

    return retval


def _get_input_schema(context_name):
    context_def = CONTEXTS[context_name]
    field_map = _get_field_map()

    input_types = {
        "required": _get_input_types(field_map, context_def.get("required", ())),
        "optional": _get_input_types(field_map, context_def.get("optional", ()))
    }

    return input_types


def _get_return_fields(context_name):
    context_def = CONTEXTS[context_name]

    if "return" in context_def:
        return context_def.get("return", ())
    else:
        return context_def.get("required", ()) + context_def.get("optional", ())


def _get_return_schema(context_name):
    field_map = _get_field_map()
    return_fields = _get_return_fields(context_name)

    return_types = tuple(field_map[field][1] for field in return_fields)
    return_names = tuple(field_map[field][0] for field in return_fields)

    return return_types, return_names


def create_context_schema(context_name):
    input_types = _get_input_schema(context_name)
    return_types, return_names = _get_return_schema(context_name)

    return input_types, return_types, return_names


def init_context(context, **kwargs):
    field_map = _get_field_map()
    retval = {}

    workflow_config = kwargs.get("workflow_config", None)

    if workflow_config is None and context and "workflow_config" in context:
        workflow_config = context["workflow_config"]

    if workflow_config:
        for key in WORKFOW_SETTINGS_KEYS:
            if key in workflow_config:
                retval[key] = workflow_config[key]

    for idx in field_map:
        if idx == "context":
            continue

        if idx in WORKFOW_SETTINGS_KEYS and idx in retval:
            val = kwargs.get(idx, None)
            if val is not None:
                retval[idx] = val
            continue

        val = kwargs[idx] if idx in kwargs else None
        if val is not None:
            retval[idx] = val
        elif context and idx in context:
            retval[idx] = context[idx]
        else:
            retval[idx] = None

    if any(k in retval for k in WORKFOW_SETTINGS_KEYS):
        retval["workflow_config"] = {
            "seed": retval.get("seed"),
            "steps": retval.get("steps"),
            "cfg": retval.get("cfg"),
            "sampler_name": retval.get("sampler_name"),
            "scheduler": retval.get("scheduler"),
            "clip_l_positive": retval.get("clip_l_positive"),
            "clip_g_positive": retval.get("clip_g_positive"),
            "t5xxl_positive": retval.get("t5xxl_positive"),
            "clip_l_negative": retval.get("clip_l_negative"),
            "clip_g_negative": retval.get("clip_g_negative"),
            "t5xxl_negative": retval.get("t5xxl_negative"),
            "guidance": retval.get("guidance"),
            "ascore_positive": retval.get("ascore_positive"),
            "ascore_negative": retval.get("ascore_negative"),
            "target_width": retval.get("target_width"),
            "target_height": retval.get("target_height"),
        }
    else:
        retval["workflow_config"] = workflow_config

    return retval


def build_return_tuple(context_name, args):
    context_fields = _get_return_fields(context_name)
    return tuple([args] + [args.get(field) for field in context_fields if field != "context"])
