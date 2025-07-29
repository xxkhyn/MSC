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
        self.yakus = {}  # 役名 → 翻数 の辞書

    def add_yaku(self, name):
        double_yakuman = {
            "純正九蓮宝燈",
            "国士無双十三面待ち",
            "四暗刻単騎",
            "大四喜",
        }
        han = 26 if name in double_yakuman else 13
        self.yakus[name] = han

    def remove_yaku(self, name):
        if name in self.yakus:
            del self.yakus[name]

    def get_count(self):
        return len(self.yakus)

    def get_yakus(self):
        return self.yakus
    
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
    yakuman_names = set(yakumann.get_yakus().keys())  # ←ここがポイント

    if yakuman_names:
        # 役満があれば通常役は全部消す
        for name in list(yaku_names):
            yaku_counter.remove_yaku(name)
        return

    for upper, lowers in CONFLICT_RULES.items():
        if upper in yaku_names:
            for lower in lowers:
                if lower in yaku_names:
                    yaku_counter.remove_yaku(lower)

