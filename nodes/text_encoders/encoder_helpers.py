# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

def encode_prompts_flux(clip, clip_l_positive, t5xxl_positive, clip_l_negative, t5xxl_negative, guidance):
    positive_tokens = clip.tokenize(clip_l_positive)
    positive_tokens["t5xxl"] = clip.tokenize(t5xxl_positive)["t5xxl"]
    negative_tokens = clip.tokenize(clip_l_negative)
    negative_tokens["t5xxl"] = clip.tokenize(t5xxl_negative)["t5xxl"]

    return (
        clip.encode_from_tokens_scheduled(
            positive_tokens,
            add_dict={"guidance": guidance, }
        ),
        clip.encode_from_tokens_scheduled(
            negative_tokens,
            add_dict={"guidance": guidance, }
        )
    )


def encode_prompts_sdxl(clip, clip_l_positive, clip_g_positive, clip_l_negative, clip_g_negative,
                        ascore_positive, ascore_negative, width, height, target_width, target_height):
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
