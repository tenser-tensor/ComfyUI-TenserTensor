# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import comfy.samplers as S


class Guider_Basic(S.CFGGuider):
    def set_conds(self, positive):
        self.inner_set_conds({"positive": positive})


def encode_prompts_sdxl(clip, clip_l_positive, clip_g_positive, clip_l_negative, clip_g_negative,
                        ascore_positive, ascore_negative, width, height, target_width, target_height):
    if clip is None:
        raise ValueError("ERROR: CLIP is required for text encoder")

    positive_tokens = clip.tokenize(clip_g_positive)
    positive_tokens["l"] = clip.tokenize(clip_l_positive)["l"]
    negative_tokens = clip.tokenize(clip_g_negative)
    negative_tokens["l"] = clip.tokenize(clip_l_negative)["l"]

    return (
        clip.encode_from_tokens_scheduled(
            positive_tokens,
            add_dict={
                "aesthetic_score": ascore_positive,
                "width": width,
                "height": height,
                "target_width": target_width,
                "target_height": target_height,
            }
        ),
        clip.encode_from_tokens_scheduled(
            negative_tokens,
            add_dict={
                "aesthetic_score": ascore_negative,
                "width": width,
                "height": height,
                "target_width": target_width,
                "target_height": target_height,
            }
        )
    )


def encode_prompts_flux(clip, clip_l_positive, t5xxl_positive, clip_l_negative, t5xxl_negative, guidance):
    if clip is None:
        raise ValueError("ERROR: CLIP is required for text encoder")

    positive_tokens = clip.tokenize(clip_l_positive)
    positive_tokens["t5xxl"] = clip.tokenize(t5xxl_positive)["t5xxl"]
    negative_tokens = clip.tokenize(clip_l_negative)
    negative_tokens["t5xxl"] = clip.tokenize(t5xxl_negative)["t5xxl"]

    return (
        clip.encode_from_tokens_scheduled(positive_tokens, add_dict={"guidance": guidance, }),
        clip.encode_from_tokens_scheduled(negative_tokens, add_dict={"guidance": guidance, })
    )


def encode_prompts_flux2(model, clip, prompt, lora_triggers, guidance):
    if clip is None:
        raise ValueError("ERROR: CLIP is required for text encoder")

    tokens = clip.tokenize(f"{lora_triggers}, {prompt}")
    conditioning = clip.encode_from_tokens_scheduled(tokens, add_dict={"guidance": guidance, })
    guider = Guider_Basic(model)
    guider.set_conds(conditioning)

    return (guider,)
