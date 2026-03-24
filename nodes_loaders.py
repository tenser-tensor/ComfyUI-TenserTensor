# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import os
from typing import override, Any

import torch

import folder_paths
from comfy import samplers, sd, ldm, utils, model_management
from comfy_api.latest import io
from nodes import VAELoader
from .gguf import utils as gguf_utils
from .utils import raise_unless, CommonTypes

CATEGORY = "TenserTensor/Loaders"

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
        conds = {"positive": positive}
        if negative is not None:
            conds["negative"] = negative

        self.inner_set_conds(conds)

    def get_conds(self, key="positive"):
        return [[c.get("cross_attn", None), c] for c in self.original_conds[key]]


class LoraCache:
    def __init__(self):
        self.cache: dict[str, Any] = {}

    def get(self, key: str, default=None):
        return self.cache.get(key, default)

    def set(self, key: str, value) -> None:
        self.cache[key] = value


lora_cache = LoraCache()


# ==============================================================================
# File list utilities — folder_paths wrappers for model file discovery
# ==============================================================================

def update_folder_names_and_paths(folder, base_folder=None, exts=None):
    if folder in folder_paths.folder_names_and_paths:
        return

    path = os.path.join(folder_paths.models_dir, folder)
    os.makedirs(path, exist_ok=True)
    paths = [path]
    base_paths, base_exts = folder_paths.folder_names_and_paths.get(base_folder, ([], {})) if base_folder else ([], {})
    _exts = exts if exts is not None else base_exts
    folder_paths.folder_names_and_paths[folder] = (paths + base_paths, _exts)


def get_gguf_diffusion_models_files():
    update_folder_names_and_paths("diffusion_models_gguf", "diffusion_models", {".gguf"})

    return [x for x in folder_paths.get_filename_list("diffusion_models_gguf")]


def get_gguf_text_encoder_files():
    update_folder_names_and_paths("text_encoders_gguf", "text_encoders", {'.gguf', '.pt', '.pth', '.safetensors'})

    return [x for x in folder_paths.get_filename_list("text_encoders_gguf")]


def get_gguf_clip_vision_files():
    update_folder_names_and_paths("clip_vision_gguf", "clip_vision", {'.gguf', '.pt', '.pth', '.safetensors'})

    return ["None", *[x for x in folder_paths.get_filename_list("clip_vision_gguf")]]


def get_lora_files():
    return ["None"] + folder_paths.get_filename_list("loras")


def get_vae_files():
    return VAELoader.vae_list(VAELoader)


# ==============================================================================
# Helper functions — pipeline utilities and loaders
# ==============================================================================

def apply_lora(cached_lora, model, clip, filename, strength):
    if cached_lora is None:
        lora_path = folder_paths.get_full_path_or_raise("loras", filename)
        lora = utils.load_torch_file(lora_path, safe_load=True)
    else:
        lora = cached_lora

    if isinstance(model, gguf_utils.GGUFModelPatcher):
        patched_model, patched_text_encoder = sd.load_bypass_lora_for_models(model, clip, lora, strength, strength)
    else:
        patched_model, patched_text_encoder = sd.load_lora_for_models(model, clip, lora, strength, strength)

    return patched_model, patched_text_encoder, lora


def apply_lora_stack(cls, model, clip, **kwargs):
    apply_loras = kwargs.get("apply_loras", True)
    apply_lora_stack = kwargs.get("apply_lora_stack", {})

    if apply_loras or apply_lora_stack.get("apply_lora_stack") == "Patch":
        loras = [
            ("distilled_lora", "distilled_lora_strength", f"{cls.__name__}_distilled_lora",),
            ("lora_name_1", "strength_1", f"{cls.__name__}_loaded_lora_1",),
            ("lora_name_2", "strength_2", f"{cls.__name__}_loaded_lora_2",),
            ("lora_name_3", "strength_3", f"{cls.__name__}_loaded_lora_3",),
            ("lora_name_4", "strength_4", f"{cls.__name__}_loaded_lora_4",),
        ]

        for name, strength, cache_key in loras:
            filename = apply_lora_stack.get(name, "None") or kwargs.get(name, "None")
            strength_value = apply_lora_stack.get(strength, 0.0) or kwargs.get(strength, 0.0)
            if filename != "None" and strength_value != 0.0:
                cached = lora_cache.get(cache_key)
                model, clip, lora = apply_lora(cached, model, clip, filename, strength_value)
                lora_cache.set(cache_key, lora)

    return model, clip


def load_vae(vae_name, **kwargs):
    vae_dtype = "default"
    load_device = model_management.vae_device()
    extended_params = kwargs.get("extended_params")
    if extended_params.get("extended_params") == "Manual":
        if extended_params.get("vae_device") != "cpu":
            vae_dtype = extended_params.get("vae_dtype")
        if extended_params.get("vae_device") == "cpu":
            load_device = torch.device("cpu")

    weight_dtype = CommonTypes.TORCH_DTYPES[vae_dtype]
    vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
    state_dict, metadata = utils.load_torch_file(vae_path, return_metadata=True)

    if "vocoder.vocoder.conv_post.weight" in state_dict:
        vae = ldm.lightricks.vae.audio_vae.AudioVAE(state_dict, metadata)
    else:
        vae = sd.VAE(sd=state_dict, device=load_device, dtype=weight_dtype, metadata=metadata)
        vae.throw_exception_if_invalid()

    return vae


def ltxv_gguf_pipeline(cls, **kwargs):
    model = gguf_utils.load_diffusion_model_gguf(**kwargs)
    text_encoder = gguf_utils.load_text_encoders_gguf(sd.CLIPType.LTXV, **kwargs)
    model, text_encoder = apply_lora_stack(cls, model, text_encoder, **kwargs)

    video_vae_name, audio_vae_name = kwargs.get("video_vae"), kwargs.get("audio_vae")
    video_vae = load_vae(video_vae_name, **kwargs)
    audio_vae = load_vae(audio_vae_name, **kwargs)

    raise_unless(
        isinstance(video_vae, sd.VAE),
        ValueError,
        f"Invalid Video VAE model type, selected wrong file {video_vae_name}"
    )
    raise_unless(
        isinstance(audio_vae, ldm.lightricks.vae.audio_vae.AudioVAE),
        ValueError,
        f"Invalid Audio VAE model type, selected wrong file {audio_vae_name}"
    )

    return model, text_encoder, video_vae, audio_vae


# ==============================================================================
# Node classes — ComfyUI node definitions
# ==============================================================================

class TT_LtxvGgufModelsLoaderNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_LtxvGgufModelsLoaderNode",
            display_name="TT LTXV GGUF Models Loader",
            category=CATEGORY,
            description="",
            inputs=[
                io.Combo.Input("diffusion_model", options=get_gguf_diffusion_models_files()),
                io.Combo.Input("text_encoder", options=get_gguf_text_encoder_files()),
                io.Combo.Input("embeddings_connector", options=get_gguf_text_encoder_files()),
                io.Combo.Input("distilled_lora", options=get_lora_files()),
                io.Float.Input("distilled_lora_strength", default=1.0, min=-10.0, max=10.0, step=0.1),
                io.Combo.Input("video_vae", options=get_vae_files()),
                io.Combo.Input("audio_vae", options=get_vae_files()),
                io.DynamicCombo.Input("extended_params", options=[
                    io.DynamicCombo.Option("Defaults", []),
                    io.DynamicCombo.Option("Manual", [
                        io.Combo.Input("model_dequant_dtype", options=list(CommonTypes.TORCH_DTYPES.keys()), default="bfloat16"),
                        io.Combo.Input("model_patch_dtype", options=list(CommonTypes.TORCH_DTYPES.keys()), default="bfloat16"),
                        io.Boolean.Input("model_patch_on_device", default=False, label_on="Load Device", label_off="Unload Device"),
                        io.Boolean.Input("allow_fp16_accumulation", default=False, label_on="Half Precision", label_off="Full Precision"),
                        io.Combo.Input("attention_override", options=["None"] + list(gguf_utils.ATTENTION_OVERRIDES.keys()), default=None),
                        io.Combo.Input("text_encoder_device", options=CommonTypes.TORCH_DEVICES, default="default"),
                        io.Combo.Input("vae_device", options=CommonTypes.TORCH_DEVICES, default="default"),
                        io.Combo.Input("vae_dtype", options=list(CommonTypes.TORCH_DTYPES.keys())),
                    ]),
                ]),
            ],
            outputs=[
                io.Model.Output("MODEL"),
                io.Clip.Output("TEXT_ENCODER"),
                io.Vae.Output("VIDEO_VAE"),
                io.Vae.Output("AUDIO_VAE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        model, text_encoder, video_vae, audio_vae = ltxv_gguf_pipeline(cls, **kwargs)

        return io.NodeOutput(model, text_encoder, video_vae, audio_vae)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

NODES = [
    TT_LtxvGgufModelsLoaderNode,
]
