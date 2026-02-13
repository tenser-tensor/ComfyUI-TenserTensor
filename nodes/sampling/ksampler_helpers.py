import comfy
import latent_preview
import torch


def sample_latents(**kwargs):
    model = kwargs.get("model", None)
    latent = kwargs.get("latent", None)

    if model is None:
        raise ValueError("Model is required for sampling")
    if latent is None:
        raise ValueError("Latent image is required for sampling")

    steps = kwargs.get("steps", 0)
    seed = kwargs.get("seed", 0)

    latent_img = comfy.sample.fix_empty_latent_channels(model, latent["samples"])

    add_noise = kwargs.get("add_noise", True)
    if add_noise:
        bat_idx = latent.get("batch_index", None)
        noise = comfy.sample.prepare_noise(latent_img, seed, bat_idx)
    else:
        noise = torch.zeros(latent_img.size(), dtype=latent_img.dtype, layout=latent_img.layout, device="cpu")

    callback = latent_preview.prepare_callback(model, steps)

    args = {
        "model": model,
        "noise": noise,
        "steps": steps,
        "cfg": kwargs.get("cfg", 0),
        "sampler_name": kwargs.get("sampler_name", None),
        "scheduler": kwargs.get("scheduler", None),
        "positive": kwargs.get("positive", None),
        "negative": kwargs.get("negative", None),
        "latent_image": latent_img,
        "denoise": kwargs.get("denoise", 1.0),
        "disable_noise": not add_noise,
        "start_step": kwargs.get("start_step", 0),
        "last_step": kwargs.get("last_step", 10000),
        "force_full_denoise": kwargs.get("full_denoise", True),
        "noise_mask": latent.get("noise_mask", None),
        "disable_pbar": not comfy.utils.PROGRESS_BAR_ENABLED,
        "callback": callback,
        "seed": seed,
    }

    samples = comfy.sample.sample(**args)

    retval = latent.copy()
    retval["samples"] = samples

    return retval
