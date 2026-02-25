# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import torch


def vae_encode(image, vae, tile_width=512, tile_height=512, overlap=64):
    samples = vae.encode_tiled(
        image,
        tile_x=tile_width,
        tile_y=tile_height,
        overlap=overlap
    )
    latent_dict = {"samples": samples}

    return latent_dict


def vae_decode(latent, vae, tile_width=512, tile_height=512, overlap=64, circular=False):
    samples = latent["samples"]
    if samples.is_nested:
        samples = samples.unbind()[0]

    if circular == True:
        for layer in [layer for layer in vae.first_stage_model.modules() if isinstance(layer, torch.nn.Conv2d)]:
            layer.padding_mode = "circular"

    compression = vae.spacial_compression_decode()
    images = vae.decode_tiled(
        samples,
        tile_x=tile_width // compression,
        tile_y=tile_height // compression,
        overlap=overlap // compression
    )

    if len(images.shape) == 5:
        images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])

    return images
