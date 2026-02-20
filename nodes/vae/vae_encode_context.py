# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

class TT_VaeEncodeContext:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "context": ("TT_CONTEXT",),
            }
        }

    RETURN_TYPES = ("TT_CONTEXT", "LATENT",)
    RETURN_NAMES = ("CONTEXT", "LATENT",)
    FUNCTION = "vae_encode"
    CATEGORY = "TenserTensor/VAE"

    def vae_encode(self, context):
        vae = context["vae"]
        image = context["image"]

        if vae is None:
            raise ValueError("VAE is required for encode")
        if image is None:
            raise ValueError("Pixel image is required for encode")

        samples = vae.encode(image)
        latent_dict = {"samples": samples}
        context["latent"] = latent_dict

        return (context, latent_dict,)
