# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)


import comfy.samplers as S


class BasicGuider(S.CFGGuider):
    def set_conds(self, conditioning):
        self.inner_set_conds({"positive": conditioning})

    def get_conds(self, key="positive"):
        return [[c.get("cross_attn", None), c] for c in self.original_conds[key]]


class CommonTypes():
    MEGAPIXELS = ["0.25 MP", "0.5 MP", "1 MP", "2 MP", "4 MP", "8 MP"]
