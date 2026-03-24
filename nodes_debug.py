# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import json

from comfy_api.latest import io, ui

CATEGORY = "TenserTensor/_debug"


# def load_audio_vae(**kwargs):
#     vae_path = folder_paths.get_full_path_or_raise("vae", kwargs.get("vae_name"))
#     load_device = model_management.vae_device()
#     vae_dtype = torch.float32
#
#     extended_params = kwargs.get("extended_params")
#     if extended_params.get("extended_params") == "Manual":
#         if extended_params.get("vae_device") == "cpu":
#             load_device = torch.device("cpu")
#         _dtype = extended_params.get("vae_dtype")
#         if _dtype != "default":
#             vae_dtype = CommonTypes.TORCH_DTYPES[_dtype]
#
#     state_dict, metadata = utils.load_torch_file(vae_path, return_metadata=True)
#     vae = sd.VAE(sd=state_dict, device=load_device, dtype=vae_dtype, metadata=metadata)
#     # vae = AudioVAE(state_dict=state_dict, metadata=metadata)
#
#     return vae
#
#
# def stable_audio_pipeline(**kwargs):
#     load_mode = kwargs.get('load_mode')
#     if load_mode.get("load_mode") == "Checkpoint":
#         print(f"CHECKPOINT: {load_mode.get("checkpoint")}")
#         ckpt_path = folder_paths.get_full_path_or_raise("checkpoints", load_mode.get("checkpoint"))
#
#         out = sd.load_checkpoint_guess_config(
#             ckpt_path,
#             output_vae=True,
#             output_clip=True,
#             embedding_directory=get_embedding_directory()
#         )
#
#         model, clip, vae = out[:3]
#     else:
#         model = load_diffusion_model(load_mode.get("diffusion_model"))
#         clip = load_text_encoders([load_mode.get("t5base")], sd.CLIPType.STABLE_AUDIO)
#         vae = load_audio_vae(**kwargs)
#
#     return model, clip, vae
#
#
# class TT_StableAudioOpenModelsLoaderNode(io.ComfyNode):
#     @classmethod
#     def define_schema(cls) -> io.Schema:
#         return io.Schema(
#             node_id="TT_StableAudioOpenModelsLoaderNode",
#             display_name="TT Stable Audio Open Models Loader",
#             category=CATEGORY,
#             description="",
#             inputs=[
#                 io.DynamicCombo.Input("load_mode", options=[
#                     io.DynamicCombo.Option("Checkpoint", [
#                         io.Combo.Input("checkpoint", options=get_checkpoint_files()),
#                     ]),
#                     io.DynamicCombo.Option("Separate", [
#                         io.Combo.Input("diffusion_model", options=get_diffusion_models_files()),
#                         io.Combo.Input("t5base", options=get_text_encoder_files()),
#                         io.Combo.Input("vae_name", options=get_vae_files()),
#                     ]),
#                 ]),
#                 io.DynamicCombo.Input("extended_params", options=[
#                     io.DynamicCombo.Option("Defaults", []),
#                     io.DynamicCombo.Option("Manual", [
#                         io.Boolean.Input("clip_device", default=False, label_on="CPU", label_off="Default"),
#                         io.Boolean.Input("vae_device", default=False, label_on="CPU", label_off="Default"),
#                         io.Combo.Input("vae_dtype", options=list(CommonTypes.TORCH_DTYPES.keys()), default="default"),
#                     ]),
#                 ]),
#             ],
#             outputs=[
#                 io.Model.Output("MODEL"),
#                 io.Clip.Output("CLIP"),
#                 io.Vae.Output("VAE"),
#             ]
#         )
#
#     @classmethod
#     def execute(cls, **kwargs) -> io.NodeOutput:
#         model, clip, vae = stable_audio_pipeline(**kwargs)
#
#         return io.NodeOutput(model, clip, vae)
#
#
# class TT_AudioLatentFactoryNode(io.ComfyNode):
#     @classmethod
#     def define_schema(cls) -> io.Schema:
#         return io.Schema(
#             node_id="TT_AudioLatentFactoryNode",
#             display_name="TT Audio Latent Factory",
#             category=CATEGORY,
#             description="",
#             inputs=[
#                 io.Float.Input("seconds", default=47.6, min=1.0, max=1000.0, step=0.1),
#                 io.Int.Input("batch_size", default=1, min=1, max=4096),
#             ],
#             outputs=[
#                 io.Latent.Output("LATENT"),
#             ],
#         )
#
#     @classmethod
#     def execute(cls, **kwargs) -> io.NodeOutput:
#         length = round((kwargs.get("seconds") * 44100 / 2048) / 2) * 2
#         latent = torch.zeros([kwargs.get("batch_size"), 64, length], device=model_management.intermediate_device())
#
#         return io.NodeOutput({"samples": latent, "type": "audio"})
#
#
# class TT_AudioSaverNode(io.ComfyNode):
#     @classmethod
#     def define_schema(cls) -> io.Schema:
#         return io.Schema(
#             node_id="TT_AudioSaverNode",
#             display_name="TT Audio Saver",
#             category=CATEGORY,
#             description="",
#             inputs=[],
#             outputs=[],
#         )
#
#     @classmethod
#     def execute(cls, **kwargs) -> io.NodeOutput:
#         # FLAC / MP3 / Opus
#         raise NotImplementedError


def json_to_markdown(value, key=None, markdown="", level=0):
    if key:
        level += 1

    tab = "  " * level
    match value:
        case dict():
            markdown += f"- {key}: {{\n" if key else "- {\n"
            for k, v in value.items():
                markdown += json_to_markdown(v, k, level=level)
            markdown += "}\n"
        case list():
            markdown += f"- **{key}**: [\n" if key else "- [\n"
            for val in value:
                markdown += json_to_markdown(value=val, level=level)
            markdown += "\n"
        case _:
            if key:
                markdown += f"{tab}- **{key}**: {value}\n"
            else:
                markdown += f"{tab}- {value}\n"

    return markdown


def decode_json(json_string):
    try:
        parsed = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e.msg} Line: {e.lineno} Column: {e.colno}")

    return json_to_markdown(parsed)


class TT_JsonPreviewDebugNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_JsonPreviewDebugNode",
            display_name="TT JSON Preview (Debug)",
            category=CATEGORY,
            description="",
            inputs=[
                io.String.Input("debug_info", force_input=True),
            ],
            outputs=[
                io.String.Output("markdown")
            ],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        debug_info = kwargs.get("debug_info")
        markdown = decode_json(debug_info)

        return io.NodeOutput(markdown, ui=ui.PreviewText(markdown))






NODES = [
    # TT_StableAudioOpenModelsLoaderNode,
    # TT_AudioLatentFactoryNode,
    TT_JsonPreviewDebugNode,
    # TT_AudioSaverNode,
]
