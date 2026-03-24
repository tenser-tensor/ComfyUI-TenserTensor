# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)


from typing import override

from comfy import samplers
from comfy_api.latest import io
from node_helpers import conditioning_set_values
from .utils import raise_unless, CommonTypes

CATEGORY = "TenserTensor/Text Encoder"


# ==============================================================================
# Helper classes — data structures and base types
# ==============================================================================


class AdaptiveCFGGuider(samplers.CFGGuider):
    @classmethod
    def from_cfg_guider(cls, guider):
        obj = cls.__new__(cls)
        obj.__dict__.update(guider.__dict__)

        return obj

    @override
    def set_conds(self, positive, negative=None):
        dict = {"positive": positive}
        if negative is not None:
            dict["negative"] = negative

        self.inner_set_conds(dict)

    def get_conds(self, key="positive"):
        return [[c.get("cross_attn", None), c] for c in self.original_conds[key]]


# ==============================================================================
# Helper functions — pipeline utilities and loaders
# ==============================================================================

def ltxv_prepare_conditioning(**kwargs):
    model = kwargs.get("model")
    raise_unless(model, ValueError, "MODEL is required for text encoder")
    text_encoder = kwargs.get("text_encoder")
    raise_unless(text_encoder, ValueError, "TEXT ENCODER is required for text encoder")
    use_prompts = kwargs.get("use_prompts")
    positive_prompt, negative_prompt = (
        use_prompts.get("positive_prompt"),
        use_prompts.get("negative_prompt"),
    )

    generated_prompt_tokens = None
    positive_tokens = generated_prompt_tokens or text_encoder.tokenize(positive_prompt)
    negative_tokens = text_encoder.tokenize(negative_prompt)
    fps = int(kwargs.get("frame_rate").replace("fps", ""))
    positive = conditioning_set_values(text_encoder.encode_from_tokens_scheduled(positive_tokens), {"frame_rate": fps})
    negative = conditioning_set_values(text_encoder.encode_from_tokens_scheduled(negative_tokens), {"frame_rate": fps})

    guider = AdaptiveCFGGuider(model)
    guider.set_conds(positive, negative)
    guider.set_cfg(kwargs.get("cfg"))

    return guider, positive, negative


# ==============================================================================
# Node classes — ComfyUI node definitions
# ==============================================================================


class TT_LtxvTextEncodeNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LtxvTextEncodeNode",
            display_name="TT LTXV Text Encode",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Clip.Input("text_encoder"),
                io.Float.Input("cfg", default=3.5, min=0.0, max=20.0, step=0.1),
                io.Combo.Input("frame_rate", options=CommonTypes.FRAME_RATES, default="24fps"),
                io.DynamicCombo.Input("use_prompts", options=[
                    io.DynamicCombo.Option("Internal", [
                        io.String.Input("positive_prompt", multiline=True, dynamic_prompts=True),
                        io.String.Input("negative_prompt", multiline=True, dynamic_prompts=True),
                    ]),
                    io.DynamicCombo.Option("External", [
                        io.String.Input("positive_prompt", force_input=True),
                        io.String.Input("negative_prompt", force_input=True),
                    ]),
                ]),
            ],
            outputs=[
                io.Guider.Output("GUIDER"),
                io.Conditioning.Output("POSITIVE"),
                io.Conditioning.Output("NEGATIVE"),
            ],
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        guider, positive, negative = ltxv_prepare_conditioning(**kwargs)

        return io.NodeOutput(guider, positive, negative)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================


NODES = [
    TT_LtxvTextEncodeNode,
]
