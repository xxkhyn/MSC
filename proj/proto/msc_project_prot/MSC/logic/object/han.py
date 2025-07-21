class YakuCounter:
    def __init__(self):
        self.yakus = {}  # 役名ごとの翻数を格納
        self.total_han = 0  # 合計翻数

    def add_yaku(self, name, han, is_yakuman=False):
        self.yakus[name] = self.yakus.get(name, 0) + han
        if is_yakuman:
            self.total_han = 13  # 役満なら上書き or 固定
        else:
            self.total_han += han


    def get_total(self):
        return self.total_han

    def get_yakus(self):
        return self.yakus

class Yakumann:
    def __init__(self):
        self.yakus = {}  # 役満一つおきに格納
        self.total_han = 0  # 合計役満数

    def add_yaku(self, name, han):
        if name not in self.yakus:
            self.yakus[name] = han
        else:
            self.yakus[name] += han
        self.total_han += han

    def get_total(self):
        return self.total_han

    def get_yakus(self):
        return self.yakus
