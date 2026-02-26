# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import dataclasses
from dataclasses import dataclass

from comfy.samplers import KSampler


@dataclass
class TTWorkflowSettings():
    seed: int | None = None
    steps: int | None = None
    cfg: int | None = None
    sampler_name: list[str] | None = None
    scheduler_name: list[str] | None = None
    clip_l_positive: str | None = None
    clip_g_positive: str | None = None
    t5xxl_positive: str | None = None
    clip_l_negative: str | None = None
    clip_g_negative: str | None = None
    t5xxl_negative: str | None = None
    guidance: float | None = None
    ascore_positive: float | None = None
    ascore_negative: float | None = None
    width: int | None = None
    height: int | None = None
    target_width: int | None = None
    target_height: int | None = None

    @classmethod
    def create(cls, **kwargs):
        wf = cls()
        for field in dataclasses.fields(wf):
            setattr(wf, field.name, kwargs.get(field.name, None))

        setattr(wf, "sampler_name", KSampler.SAMPLERS)
        setattr(wf, "scheduler_name", KSampler.SCHEDULERS)

        return wf

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
