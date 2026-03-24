# (c) TenserTensor <tenser.tensor@proton.me> || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from comfy_api.latest import io, ComfyExtension

from .nodes_context import Context

CATEGORY = "TenserTensor/VAE"

TILE_SIZE, OVERLAP = 512, 64


def vae_decode(latent, vae, tile_width=TILE_SIZE, tile_height=TILE_SIZE, overlap=OVERLAP):
    samples = latent["samples"]

    compression = vae.spacial_compression_decode()
    image = vae.decode_tiled(
        samples,
        tile_x=tile_width // compression,
        tile_y=tile_height // compression,
        overlap=overlap // compression
    )

    return image


def vae_encode(image, vae, tile_width=TILE_SIZE, tile_height=TILE_SIZE, overlap=OVERLAP):
    samples = vae.encode_tiled(
        image,
        tile_x=tile_width,
        tile_y=tile_height,
        overlap=overlap
    )

    return {"samples": samples}


class TT_VaeDecodeTiledNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_VaeDecodeTiledNode",
            display_name="TT Vae Decode (Tiled)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Vae.Input("vae"),
                io.Latent.Input("latent"),
                io.Int.Input("tile_width", default=512, min=64, max=4096, step=64),
                io.Int.Input("tile_height", default=512, min=64, max=4096, step=64),
                io.Int.Input("overlap", default=64, min=8, max=256, step=8),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        image = vae_decode(**kwargs)

        return io.NodeOutput(image)


class TT_VaeDecodeContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_VaeDecodeContextNode",
            display_name="TT Vae Decode (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context"),
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Image.Output("IMAGE"),
            ]
        )

    @classmethod
    def execute(cls, context) -> io.NodeOutput:
        vae = context.get("vae")
        if vae is None:
            raise ValueError("ERROR: VAE is required for decode")

        latent = context.get("latent")
        if latent is None:
            raise ValueError("ERROR: Latent image is required for decode")

        image = vae_decode(latent, vae)

        return io.NodeOutput(context, image)


class TT_VaeEncodeTiledNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_VaeEncodeTiledNode",
            display_name="TT Vae Encode (Tiled)",
            category=CATEGORY,
            description="",
            inputs=[
                io.Image.Input("image"),
                io.Vae.Input("vae"),
                io.Int.Input("tile_width", default=512, min=64, max=4096, step=64),
                io.Int.Input("tile_height", default=512, min=64, max=4096, step=64),
                io.Int.Input("overlap", default=64, min=8, max=256, step=8),
            ],
            outputs=[
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        latent = vae_encode(**kwargs)

        return io.NodeOutput(latent)


class TT_VaeEncodeContextNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TT_VaeEncodeContextNode",
            display_name="TT Vae Encode (Context)",
            category=CATEGORY,
            description="",
            inputs=[
                Context.Input("context"),
            ],
            outputs=[
                Context.Output("CONTEXT"),
                io.Latent.Output("LATENT"),
            ]
        )

    @classmethod
    def execute(cls, context) -> io.NodeOutput:
        vae = context.get("vae")
        if vae is None:
            raise ValueError("ERROR: VAE is required for encode")

        image = context.get("image")
        if image is None:
            raise ValueError("ERROR: Pixel image is required for encode")

        latent = vae_encode(image, vae)

        return io.NodeOutput(context, latent)


# ==============================================================================
# V3 entrypoint — registers context nodes with ComfyUI
# ==============================================================================

NODES = [
    TT_VaeDecodeTiledNode,
    TT_VaeDecodeContextNode,
    TT_VaeEncodeTiledNode,
    TT_VaeEncodeContextNode,
]
