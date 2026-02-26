# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)


import dataclasses
from dataclasses import dataclass

import comfy.samplers as S
from comfy_api.latest import IO
from .workflow_classes import TTWorkflowSettings


class BasicGuider(S.CFGGuider):
    def set_conds(self, conditioning):
        self.inner_set_conds({"positive": conditioning})

    def get_conds(self, key="positive"):
        return [[c.get("cross_attn", None), c] for c in self.original_conds[key]]


class CommonTypes():
    MEGAPIXELS = ["0.25 MP", "0.5 MP", "1 MP", "2 MP", "4 MP", "8 MP"]


@IO.comfytype(io_type="TT_WORKFLOW_CONFIG")
class WorkflowSettings:
    Type = TTWorkflowSettings

    class Input(IO.Input):
        def __init__(self, id: str, **kwargs):
            super().__init__(id, **kwargs)

    class Output(IO.Output):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


@dataclass
class TTContext():
    """
    Shared context object passed between TenserTensor context nodes.

    Holds all pipeline state as optional fields.
    All fields default to None and are populated incrementally as the workflow progresses.

    Use create() to instantiate from kwargs, and set_attr/get_attr for safe field access.
    Workflow config fields are accessible via set_workflow_config_attr/get_workflow_config_attr.
    """
    model: IO.Model | None = None
    clip: IO.Clip | None = None
    vae: IO.Vae | None = None
    guider: IO.Guider | None = None
    latent: IO.Latent | None = None
    positive: IO.Conditioning | None = None
    negative: IO.Conditioning | None = None
    conditioning: IO.Conditioning | None = None
    image: IO.Image | None = None
    mask: IO.Mask | None = None
    control_net: IO.ControlNet | None = None
    workflow_config: WorkflowSettings | None = None
    sampler_name: IO.String | None = None
    sampler: IO.Sampler | None = None
    scheduler: list[str] | None = None
    rnd_noise: IO.Noise | None = None
    sigmas: IO.Sigmas | None = None

    @classmethod
    def create(cls, **kwargs):
        ctx = cls()
        for field in dataclasses.fields(ctx):
            setattr(ctx, field.name, kwargs.get(field.name, None))

        return ctx

    @classmethod
    def get_attr_type(cls, key):
        return

    def set_attr(self, key, attr):
        if hasattr(self, key):
            setattr(self, key, attr)
        else:
            raise AttributeError(f"ERROR: Context has no attribute '{key}'")

    def get_attr(self, key, default=None):
        if hasattr(self, key):
            val = getattr(self, key)
            return val if val is not None else default
        else:
            raise AttributeError(f"ERROR: Context has no attribute '{key}'")

    def update_attrs(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                val = kwargs.get(key)
                if val is not None:
                    setattr(self, key, val)

    def set_workflow_config_attr(self, key, attr):
        if self.workflow_config:
            self.workflow_config.set_attr(key, attr)
        else:
            raise AttributeError(f"ERROR: Workflow Config is not set in context")

    def get_workflow_config_attr(self, key, default=None):
        if self.workflow_config:
            return self.workflow_config.get_attr(key, default)
        else:
            raise AttributeError(f"ERROR: Workflow Config is not set in context")

    def update_workflow_config_attrs(self, **kwargs):
        if self.workflow_config:
            for key in kwargs.keys():
                if hasattr(self.workflow_config, key):
                    val = kwargs.get(key)
                    if val is not None:
                        self.workflow_config.set_attr(key, val)
        else:
            raise AttributeError(f"ERROR: Workflow Config is not set in context")


@IO.comfytype(io_type="TT_CONTEXT")
class Context:
    Type = TTContext

    class Input(IO.Input):
        def __init__(self, id: str, **kwargs):
            super().__init__(id, **kwargs)

    class Output(IO.Output):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
