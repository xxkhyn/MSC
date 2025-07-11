"""役満と通常役をそれぞれカウントしていくクラス
重複しない役を除くことも可"""

CONFLICT_RULES = {
    # 役満内の上位互換
    "四暗刻単騎": ["四暗刻"],
    "大四喜": ["小四喜"],
    "国士無双十三面待ち": ["国士無双"],
    
    # 七対子は特殊形：面子手と排他
    "七対子": [
        "一盃口",  "対々和", "三暗刻", "三槓子", "三色同順", "三色同刻",
        "一気通貫", "混全帯么", "純全帯么", "平和"
    ],

    # 二盃口 > 一盃口
    "二盃口": ["一盃口","七対子"],

    # 対々和（暗刻が3つ含まれていても三暗刻で処理される場合）
    "対々和": ["三暗刻"],

    # 平和は構成条件が特殊で多くの役と排他（門前専用、順子構成、役牌なし）
    "平和": ["対々和", "三暗刻", "一盃口", "混全帯么", "純全帯么", "役牌", "小三元", "大三元"],

    # 混全帯么・純全帯么とタンヤオは排他（タンヤオは1・9・字牌禁止）
    "混全帯么": ["断么九"],
    "純全帯么": ["断么九"],

    # 面子系色役と一部の特殊役（必要に応じて）
    "清一色": ["混一色"],  # 両方入り得ない
    "混一色": ["清一色"],  # 逆も排他
}

class Yakumann:
    def __init__(self):
        self.yakus = set()  # 役満名のみを保持
        self.count = 0      # 役満の個数（複数役満用）

    def add_yaku(self, name):
        if name not in self.yakus:
            self.yakus.add(name)
            self.count += 1  # 役満の数をカウント

    def remove_yaku(self, name):
        if name in self.yakus:
            self.yakus.remove(name)
            self.count -= 1

    def get_count(self):
        return self.count

    def get_yakus(self):
        return list(self.yakus)

    
class YakuCounter:
    def __init__(self):
        self.yakus = {}
        self.total_han = 0

    def add_yaku(self, name, han):
        if name not in self.yakus:
            self.yakus[name] = han
        else:
            self.yakus[name] += han
        self.total_han += han

    def remove_yaku(self, name):
        if name in self.yakus:
            self.total_han -= self.yakus[name]
            del self.yakus[name]

    def get_total(self):
        return self.total_han

    def get_yakus(self):
        return self.yakus
    
def resolve_conflicts(yaku_counter: YakuCounter, yakumann: Yakumann):
    yaku_names = set(yaku_counter.get_yakus().keys())
    yakuman_names = set(yakumann.get_yakus().keys())

    # ✅ 1. 役満がある場合は通常役（翻役）をすべて削除
    if yakuman_names:
        for name in list(yaku_names):
            yaku_counter.remove_yaku(name)
        return  # 通常役すべて除去したので、個別の排他処理は不要

    # ✅ 2. 役満がない場合 → 通常のCONFLICT_RULESで排他制御
    for upper, lowers in CONFLICT_RULES.items():
        if upper in yakuman_names or upper in yaku_names:
            for lower in lowers:
                if lower in yakuman_names:
                    yakumann.remove_yaku(lower)
                if lower in yaku_names:
                    yaku_counter.remove_yaku(lower)


def resolve_conflicts(yaku_counter: YakuCounter, yakumann: Yakumann):
    yaku_names = set(yaku_counter.get_yakus().keys())
    yakuman_names = set(yakumann.get_yakus())

    for upper, lowers in CONFLICT_RULES.items():
        if upper in yakuman_names:
            for lower in lowers:
                if lower in yakuman_names:
                    yakumann.remove_yaku(lower)
                if lower in yaku_names:
                    yaku_counter.remove_yaku(lower)

        if upper in yaku_names:
            for lower in lowers:
                if lower in yaku_names:
                    yaku_counter.remove_yaku(lower)
