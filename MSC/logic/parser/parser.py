import parse_def

class ParsedHand:

    def __init__(self, tiles, winning_tile, huuro, dora):
        self.tiles = tiles
        self.winning_tile = winning_tile
        self.huuro = huuro
        self.dora = dora

"""analyze_hand_modelを引き出せばmodelsのすべての処理を引き出せる
    手牌の解析（アガれる形かどうか・面子構成の確認・）
    手牌配列と副露が別で送られてくるので、副露の情報を反映させつつ
    副露を含めた手牌を送る。

    返し値：
    解析済み手牌・アガれなかった場合のエラーアメッセージ
"""

def analyze_hand_model(hand_obj):

    hand_numeric = parse_def.tile_strs_to_indices(hand_obj.hand_pai, hand_obj.winning_pai)
    melds = parse_def.parse_huuro_to_melds(hand_obj.huuro)
    agari_patterns = parse_def.can_form_agari_numeric(hand_numeric)

    return {
        "agari_patterns": agari_patterns,
        "melds": melds,
    }

def parse_hand(hand_obj):

    return ParsedHand(
        tiles=hand_obj.hand_pai,
        winning_tile=hand_obj.winning_pai,
        huuro=hand_obj.huuro,
        dora=hand_obj.dora_pai
    )