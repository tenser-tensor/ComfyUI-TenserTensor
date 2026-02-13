class TT_VaeDecodeContext:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context": ("TT_CONTEXT",),
            }
        }

    RETURN_TYPES = ("TT_CONTEXT", "IMAGE",)
    RETURN_NAMES = ("CONTEXT", "IMAGE",)
    FUNCTION = "vae_decode"
    CATEGORY = "TenserTensor/VAE"

    def vae_decode(self, context):
        vae = context["vae"]
        latent = context["latent"]

        if vae is None:
            raise ValueError("VAE is required for decode")
        if latent is None:
            raise ValueError("Latent image is required for decode")

        samples = latent["samples"]
        if samples.is_nested:
            samples = samples.unbind()[0]

        images = vae.decode(samples)

        if len(images.shape) == 5:
            images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])

        context["image"] = images

        return (context, images,)
