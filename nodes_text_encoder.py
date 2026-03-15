# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from typing import override

from comfy import samplers
from comfy_api.latest import io
from node_helpers import conditioning_set_values
from nodes import MAX_RESOLUTION
from .nodes_context import Context
from .utils import CommonTypes, raise_if

CATEGORY = "TenserTensor/Text Encoder"


class SingleCondCFGGuider(samplers.CFGGuider):
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


def encode_prompts_sdxl(**kwargs):
    clip = kwargs.get("clip")
    raise_if(clip is None, ValueError, "CLIP is required for text encoder")

    positive_tokens = clip.tokenize(kwargs.get("clip_g_positive"))
    positive_tokens["l"] = clip.tokenize(kwargs.get("clip_l_positive"))["l"]
    negative_tokens = clip.tokenize(kwargs.get("clip_g_negative"))
    negative_tokens["l"] = clip.tokenize(kwargs.get("clip_l_negative"))["l"]

    cond_dict = {
        "aesthetic_score": kwargs.get("ascore_positive"),
        "width": kwargs.get("width"),
        "height": kwargs.get("height"),
        "target_width": kwargs.get("target_width"),
        "target_height": kwargs.get("target_height"),
    }

    positive = clip.encode_from_tokens_scheduled(positive_tokens, add_dict=cond_dict)
    cond_dict["aesthetic_score"] = kwargs.get("ascore_negative")
    negative = clip.encode_from_tokens_scheduled(negative_tokens, add_dict=cond_dict)

    return positive, negative


class TT_SdxlClipTextEncoderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_SdxlClipTextEncoderNode",
            display_name="TT SDXL CLIP Text Encoder",
            category=CATEGORY,
            description="",
            inputs=[
                io.Clip.Input("clip"),
                io.String.Input("clip_l_positive", multiline=True, placeholder="CLIP_L Positive", dynamic_prompts=True),
                io.String.Input("clip_g_positive", multiline=True, placeholder="CLIP_G Positive", dynamic_prompts=True),
                io.String.Input("clip_l_negative", multiline=True, placeholder="CLIP_L Negative", dynamic_prompts=True),
                io.String.Input("clip_g_negative", multiline=True, placeholder="CLIP_G Negative", dynamic_prompts=True),
                io.Float.Input("ascore_positive", default=9.0, min=0.0, max=100.0, step=0.1),
                io.Float.Input("ascore_negative", default=6.0, min=0.0, max=100.0, step=0.1),
                io.Int.Input("width", default=512, min=64, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=512, min=64, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_width", default=512, min=64, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_height", default=512, min=64, max=MAX_RESOLUTION, step=8),
            ],
            outputs=[
                io.Conditioning.Output("POSITIVE"),
                io.Conditioning.Output("NEGATIVE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        positive, negative = encode_prompts_sdxl(**kwargs)

        return io.NodeOutput(positive, negative)


class TT_SdxlClipTextEncoderContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_SdxlClipTextEncoderContextNode",
            display_name="TT SDXL CLIP Text Encoder (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context")
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Conditioning.Output("POSITIVE"),
                io.Conditioning.Output("NEGATIVE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        context = kwargs.get("context")

        args = {}
        for key in (
                "clip", "clip_l_positive", "clip_g_positive", "clip_l_negative", "clip_g_negative",
                "ascore_positive", "ascore_negative", "width", "height", "target_width", "target_height",
        ):
            args[key] = context.get_attr(key)

        positive, negative = encode_prompts_sdxl(**args)
        context.set_attr("positive", positive)
        context.set_attr("negative", negative)

        return io.NodeOutput(context, positive, negative)


def encode_prompts_flux(**kwargs):
    clip = kwargs.get("clip")
    raise_if(clip is None, ValueError, "CLIP is required for text encoder")

    positive_tokens = clip.tokenize(kwargs.get("clip_l_positive"))
    positive_tokens["t5xxl"] = clip.tokenize(kwargs.get("t5xxl_positive"))["t5xxl"]
    negative_tokens = clip.tokenize(kwargs.get("clip_l_negative"))
    negative_tokens["t5xxl"] = clip.tokenize(kwargs.get("t5xxl_negative"))["t5xxl"]

    guidance = kwargs.get("guidance")
    positive = clip.encode_from_tokens_scheduled(positive_tokens, add_dict={"guidance": guidance, })
    negative = clip.encode_from_tokens_scheduled(negative_tokens, add_dict={"guidance": guidance, })

    return positive, negative


class TT_Flux1ClipTextEncoderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux1ClipTextEncoderNode",
            display_name="TT FLUX1 CLIP Text Encoder",
            category=CATEGORY,
            description="",
            inputs=[
                io.Clip.Input("clip"),
                io.String.Input("clip_l_positive", multiline=True, placeholder="CLIP_L Positive", dynamic_prompts=True),
                io.String.Input("t5xxl_positive", multiline=True, placeholder="T5XXL Positive", dynamic_prompts=True),
                io.String.Input("clip_l_negative", multiline=True, placeholder="CLIP_L Negative", dynamic_prompts=True),
                io.String.Input("t5xxl_negative", multiline=True, placeholder="T5XXL Negative", dynamic_prompts=True),
                io.Float.Input("guidance", default=9.0, min=0.0, max=100.0, step=0.1),
            ],
            outputs=[
                io.Conditioning.Output("POSITIVE"),
                io.Conditioning.Output("NEGATIVE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        positive, negative = encode_prompts_flux(**kwargs)

        return io.NodeOutput(positive, negative)


class TT_Flux1ClipTextEncoderContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux1ClipTextEncoderContextNode",
            display_name="TT FLUX1 CLIP Text Encoder (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context")
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Conditioning.Output("POSITIVE"),
                io.Conditioning.Output("NEGATIVE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        context = kwargs.get("context")

        args = {}
        for key in ("clip", "clip_l_positive", "t5xxl_positive", "clip_l_negative", "t5xxl_negative", "guidance",):
            args[key] = context.get_attr(key)

        positive, negative = encode_prompts_flux(**args)
        context.set_attr("positive", positive)
        context.set_attr("negative", negative)

        return io.NodeOutput(context, positive, negative)


def encode_prompts_flux2(**kwargs):
    model, clip = kwargs.get("clip"), kwargs.get("model")
    raise_if(model is None, ValueError, "MODEL is required for text encoder")
    raise_if(clip is None, ValueError, "CLIP is required for text encoder")

    prompt, lora_triggers, guidance = (
        kwargs.get("prompt"),
        kwargs.get("lora_triggers"),
        kwargs.get("guidance"),
    )

    full_prompt = f"{lora_triggers}, {prompt}" if lora_triggers.strip() else prompt
    tokens = clip.tokenize(full_prompt)
    conditioning = clip.encode_from_tokens_scheduled(tokens, add_dict={"guidance": guidance, })
    guider = SingleCondCFGGuider(model)
    guider.set_conds(conditioning)
    guider.set_cfg(kwargs.get("cfg"))

    return guider


class TT_Flux2TextEncoderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux2TextEncoderNode",
            display_name="TT FLUX2 Text Encoder",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Clip.Input("clip"),
                io.Float.Input("cfg", default=3.0, min=0.0, max=100.0, step=0.1),
                io.String.Input("prompt", multiline=True, placeholder="Prompt", dynamic_prompts=True),
                io.String.Input("lora_triggers", multiline=True, placeholder="LoRA Triggers", dynamic_prompts=True),
                io.Float.Input("guidance", default=3.5, min=1.0, max=10.0, step=0.1)
            ],
            outputs=[
                io.Guider.Output("GUIDER"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        guider = encode_prompts_flux2(**kwargs)

        return io.NodeOutput(guider)


class TT_Flux2TextEncoderContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Flux2TextEncoderContextNode",
            display_name="TT FLUX2 Text Encoder (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context")
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Guider.Output("GUIDER"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        context = kwargs.get("context")

        args = {
            "model": context.get_attr("model"),
            "clip": context.get_attr("clip"),
            "prompt": context.get_attr("prompt"),
            "lora_triggers": context.get_attr("lora_triggers"),
            "guidance": context.get_attr("guidance"),
        }
        guider = encode_prompts_flux2(**args)
        context.set_attr("guider", guider)

        return io.NodeOutput(context, guider)


def encode_prompts_sd35(**kwargs):
    model, clip = kwargs.get("model"), kwargs.get("clip")
    raise_if(model is None, ValueError, "MODEL is required for text encoder")
    raise_if(clip is None, ValueError, "CLIP is required for text encoder")

    lora_triggers, t5xxl_positive = kwargs.get("lora_triggers"), kwargs.get("t5xxl_positive")
    if lora_triggers:
        t5xxl_positive = f"{t5xxl_positive}, {lora_triggers}"

    positive_tokens = clip.tokenize(kwargs.get("clip_g_positive"))
    positive_tokens["l"] = clip.tokenize(kwargs.get("clip_l_positive"))["l"]
    positive_tokens["t5xxl"] = clip.tokenize(t5xxl_positive)["t5xxl"]
    negative_tokens = clip.tokenize(kwargs.get("clip_g_negative"))
    negative_tokens["l"] = clip.tokenize(kwargs.get("clip_l_negative"))["l"]
    negative_tokens["t5xxl"] = clip.tokenize(kwargs.get("t5xxl_negative"))["t5xxl"]

    add_dict = {
        "width": kwargs.get("width"),
        "height": kwargs.get("height"),
        "target_width": kwargs.get("target_width"),
        "target_height": kwargs.get("target_height"),
    }

    positive = clip.encode_from_tokens_scheduled(positive_tokens, add_dict=add_dict)
    negative = clip.encode_from_tokens_scheduled(negative_tokens, add_dict=add_dict)

    guider = SingleCondCFGGuider(model)
    guider.set_conds(positive, negative)
    guider.set_cfg(kwargs.get("cfg"))

    return guider


class TT_Sd35TextEncoderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Sd35TextEncoderNode",
            display_name="TT SD3.5 Text Encoder",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Clip.Input("clip"),
                io.Float.Input("cfg", default=5.0, min=0.0, max=100.0, step=0.1),
                io.String.Input("clip_l_positive", multiline=True, placeholder="CLIP_L Positive", dynamic_prompts=True),
                io.String.Input("clip_g_positive", multiline=True, placeholder="CLIP_G Positive", dynamic_prompts=True),
                io.String.Input("t5xxl_positive", multiline=True, placeholder="T5XXL Positive", dynamic_prompts=True),
                io.String.Input("clip_l_negative", multiline=True, placeholder="CLIP_L Negative", dynamic_prompts=True),
                io.String.Input("clip_g_negative", multiline=True, placeholder="CLIP_G Negative", dynamic_prompts=True),
                io.String.Input("t5xxl_negative", multiline=True, placeholder="T5XXL Negative", dynamic_prompts=True),
                io.String.Input("lora_triggers", multiline=True, placeholder="LoRA Triggers", dynamic_prompts=True),
                io.Int.Input("width", default=512, min=0, max=MAX_RESOLUTION, step=8),
                io.Int.Input("height", default=512, min=0, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_width", default=512, min=0, max=MAX_RESOLUTION, step=8),
                io.Int.Input("target_height", default=512, min=0, max=MAX_RESOLUTION, step=8),
            ],
            outputs=[
                io.Guider.Output("GUIDER"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        guider = encode_prompts_sd35(**kwargs)

        return io.NodeOutput(guider)


class TT_Sd35TextEncoderContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Sd35TextEncoderContextNode",
            display_name="TT SD3.5 Text Encoder (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context")
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Guider.Output("GUIDER"),
            ]
        )

    @classmethod
    def execute(cls, context) -> io.NodeOutput:
        args = {}
        for key in (
                "model", "clip", "cfg",
                "clip_l_positive", "clip_g_positive", "t5xxl_positive",
                "clip_l_negative", "clip_g_negative", "t5xxl_negative",
                "lora_triggers",
                "width", "height", "target_width", "target_height",
        ):
            args[key] = context.get_attr(key)

        guider = encode_prompts_sd35(**args)
        context.set_attr("guider", guider)

        return io.NodeOutput(context, guider)


def encode_prompts_ltx23(**kwargs):
    model, clip, positive_prompt, negative_prompt, frame_rate = (
        kwargs.get("model"),
        kwargs.get("clip"),
        kwargs.get("positive_prompt"),
        kwargs.get("negative_prompt"),
        kwargs.get("frame_rate"),
    )
    positive_tokens, negative_tokens = clip.tokenize(positive_prompt), clip.tokenize(negative_prompt)
    positive = clip.encode_from_tokens_scheduled(positive_tokens)
    negative = clip.encode_from_tokens_scheduled(negative_tokens)
    positive = conditioning_set_values(positive, {"frame_rate": frame_rate})
    negative = conditioning_set_values(negative, {"frame_rate": frame_rate})

    guider = SingleCondCFGGuider(model)
    guider.set_conds(positive, negative)
    guider.set_cfg(kwargs.get("cfg"))

    return guider


class TT_Ltx23TextEncoderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_Ltx23TextEncoderNode",
            display_name="TT LTX2.3 Text Encoder",
            category=CATEGORY,
            description="",
            inputs=[
                io.Model.Input("model"),
                io.Clip.Input("clip"),
                io.Float.Input("cfg", default=1.0, min=0.0, max=100.0, step=0.1),
                io.String.Input("positive_prompt", multiline=True, placeholder="Positive Prompt", dynamic_prompts=True),
                io.String.Input("negative_prompt", multiline=True, placeholder="Negative Prompt", dynamic_prompts=True),
                io.Combo.Input("frame_rate", options=CommonTypes.FRAME_RATES, default="24fps"),
                # io.String.Input("lora_triggers", multiline=True, placeholder="LoRA Triggers", dynamic_prompts=True),
            ],
            outputs=[
                io.Guider.Output("GUIDER"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        guider = encode_prompts_ltx23(**kwargs)

        return io.NodeOutput(guider)

class TT_Ltx23TextEncoderContextNode(io.ComfyNode):
    pass

__all__ = [
    "TT_SdxlClipTextEncoderNode",
    "TT_SdxlClipTextEncoderContextNode",
    "TT_Flux1ClipTextEncoderNode",
    "TT_Flux1ClipTextEncoderContextNode",
    "TT_Flux2TextEncoderNode",
    "TT_Flux2TextEncoderContextNode",
    "TT_Sd35TextEncoderNode",
    "TT_Sd35TextEncoderContextNode",
    "TT_Ltx23TextEncoderNode",
    "TT_Ltx23TextEncoderContextNode",
]
