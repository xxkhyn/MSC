from django import forms

# 🔹 牌データ提供クラス
class HandProvider:
    def __init__(self, cleaned_data):
        self.hand_pai = [s.strip() for s in cleaned_data["hand_pai"].split(",")]

    def get_data(self):
        return self.hand_pai



# 🔹 牌解析クラス
class MahjongParser:
    @staticmethod
    def parse_tiles(tile_strs):
        tiles = [0] * 34
        for t in tile_strs:
            if t.startswith('m'):
                num = int(t[1])
                idx = num - 1
            elif t.startswith('p'):
                num = int(t[1])
                idx = 9 + (num - 1)
            elif t.startswith('s'):
                num = int(t[1])
                idx = 18 + (num - 1)
            else:
                num = int(t)
                if 1 <= num <= 7:
                    idx = 27 + (num - 1)
                else:
                    raise ValueError(f"無効な字牌指定: {t}")
            tiles[idx] += 1
        return tiles


# 🔹 データ受け取り
class DataReceiver:
    def __init__(self, provider):
        self.raw_data = provider.get_data()
        self.parsed_data = MahjongParser.parse_tiles(self.raw_data)
