# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import dataclasses
import re
from typing import override

import torch

from comfy.clip_vision import Output
from comfy_api.latest import IO, ComfyExtension, Input
from .lib.common import Context, TTContext

CATEGORY = "TenserTensor/Context"


class ContextNode(IO.ComfyNode):
    """
    Abstract base class for all context nodes.
    Handles context creation, delegation to handle(), and building return tuple.
    Subclasses should set INPUT_TYPES_DICT, RETURN_TYPES, RETURN_NAMES from a Schema,
    and override handle() to implement node-specific logic.
    """
    REQUIRED = ()
    OPTIONAL = ()
    RETURNS = ()

    F_TYPES = {}

    @classmethod
    def fill_field_types(cls):
        cls.F_TYPES = {f.name: f.type.__args__[0] for f in dataclasses.fields(TTContext)}

    @classmethod
    def inputs(cls) -> list[Input]:
        def get_input(input_name, optional):
            return Context.Input("context", optional=optional) if input_name == "context" else cls.F_TYPES[input_name].Input(input_name,
                                                                                                                             optional=optional)

        len(cls.F_TYPES) == 0 and cls.fill_field_types()
        input_schema = []

        for f_name in cls.REQUIRED:
            input_schema.append(get_input(f_name, optional=False))

        for f_name in cls.OPTIONAL:
            input_schema.append(get_input(f_name, optional=True))

        return input_schema

    @classmethod
    def outputs(cls) -> list[Output]:
        len(cls.F_TYPES) == 0 and cls.fill_field_types()
        output_schema = []

        for f_name in cls.RETURNS if len(cls.RETURNS) > 0 else cls.OPTIONAL:
            output_schema.append(
                Context.Output(display_name="CONTEXT") if f_name == "context" else cls.F_TYPES[f_name].Output(display_name=f_name.upper()))

        return output_schema

    @classmethod
    def node_output(cls, context, **kwargs) -> IO.NodeOutput:
        args = {}
        for f_name in cls.RETURNS if len(cls.RETURNS) > 0 else cls.OPTIONAL:
            if f_name != "context":
                args[f_name.upper()] = kwargs.get(f_name)

        return IO.NodeOutput(**{{"context": context}, args})

    @classmethod
    def display_name(cls):
        return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', cls.__name__.replace("TT_", "TT ").replace("Node", ""))

    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id=cls.__name__,
            display_name=cls.display_name(),
            category=CATEGORY,
            inputs=cls.inputs(),
            outputs=cls.outputs(),
        )

    @classmethod
    def handle(cls, context, **kwargs):
        return (context, kwargs,)

    @classmethod
    def execute(cls, context=None, **kwargs) -> IO.NodeOutput:
        context = TTContext.create(**kwargs) if not context else context
        context, kwargs = cls.handle(context, **kwargs)

        return cls.node_output(context, **kwargs)


class TT_BaseContextNode(ContextNode):
    """Base context node. Accepts model, clip, vae, latent and optional workflow_config."""
    REQUIRED = ("model", "clip", "vae", "latent")
    OPTIONAL = ("workflow_config",)
    RETURNS = ("context",)


class TT_BaseContextFlux2Node(ContextNode):
    """
    Base context node for FLUX2 workflows. Accepts model, clip, vae, latent, sampler, noise, and sigmas.
    Optionally accepts workflow_config. Returns context.
    """
    REQUIRED = ("model", "clip", "vae", "latent", "sampler", "rnd_noise", "sigmas",)
    OPTIONAL = ("workflow_config",)
    RETURNS = ("context",)


class TT_BaseContextPassthroughNode(ContextNode):
    """Passes context through without modification."""
    REQUIRED = ("context",)
    OPTIONAL = ()
    RETURNS = ("context",)


class ContextExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[IO.ComfyNode]]:
        return [
            TT_BaseContextNode,
            TT_BaseContextFlux2Node,
        ]


async def comfy_entrypoint() -> ContextExtension:
    return ContextExtension()


# ==============================================================================
# Re-exports for backward compatibility
# ==============================================================================

__all__ = [
    "TT_BaseContextNode",
    "TT_BaseContextFlux2Node",
    "TT_BaseContextPassthroughNode",
]
