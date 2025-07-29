from MSC.logic.object.han import YakuCounter, Yakumann, resolve_conflicts
from MSC.models import Condition

TILE_TO_INDEX = {
    **{f"m{i}": i-1 for i in range(1, 10)},
    **{f"p{i}": 9 + i-1 for i in range(1, 10)},
    **{f"s{i}": 18 + i-1 for i in range(1, 10)},
    **{f"z{i}": 27 + i-1 for i in range(1, 8)},
}

NUMERIC_TO_TILE = {v: k for k, v in TILE_TO_INDEX.items()}
def judge_yaku(parsed_hand, huuro=None,condition=None):
    """
    parsed_hand: {
        "mentsu": [...],
        "pair": {...},
        "wait": ...,
        "tiles_count": [...],  # optional
        "winning_tile_index": int,  # optional
    }
    huuro: 副露リスト

    役満と通常役を別々に判定し、排他処理の後、役名と翻数の辞書を返す。
    """

    # カウンター先に作る
    yakumann = Yakumann()
    yaku_counter = YakuCounter()

    # 和了形が成立していない場合は空の dict を返す
    if not parsed_hand.get("mentsu") or not parsed_hand.get("pair"):
        return {}

    if huuro is None:
        huuro = []

    # 役満判定関数群インポート
    from MSC.logic.yaku.yaku import (
        is_kokushi, is_kokushi_13machi, is_chinroutou, is_tsuuiisou,
        is_chuuren, is_ryuisou, is_daisuusii, is_sangenpai,
        is_suukantsu, is_suuankou, is_suuankou_tanki,
    )

    tiles_counts = parsed_hand.get("tiles_count", None)
    winning_tile_index = parsed_hand.get("winning_tile_index", None)

    # === 役満判定 ===
    if tiles_counts:
        is_kokushi(tiles_counts, yakumann)
        if winning_tile_index is not None:
            is_kokushi_13machi(tiles_counts, winning_tile_index, yakumann)
        is_chinroutou(tiles_counts, yakumann)
        is_tsuuiisou(tiles_counts, yakumann)

    is_chuuren(parsed_hand, yakumann)
    is_ryuisou(parsed_hand, yakumann)
    is_daisuusii(parsed_hand, yakumann)
    is_sangenpai(parsed_hand, yakumann)
    is_suukantsu(parsed_hand, yakumann)
    is_suuankou(parsed_hand, yakumann)
    is_suuankou_tanki(parsed_hand, yakumann)

    if yakumann.get_count() > 0:
    
        return yakumann.get_yakus()


    # === 通常役判定 ===
    from MSC.logic.yaku.yaku import (
        is_ryanpeikou,
        is_chiitoitsu, is_ikkitsuukan, is_sanshoku_doujun, is_sankantsu,
        is_sanankou, is_toitoi, is_honroutou, is_sanshoku_doukou,
        is_tanyao, is_pinfu, is_iipeikou,
    )

    is_ryanpeikou(parsed_hand, yaku_counter, huuro)
    is_chiitoitsu(tiles_counts, yaku_counter)
    is_ikkitsuukan(parsed_hand, yaku_counter, huuro)
    is_sanshoku_doujun(parsed_hand, yaku_counter, huuro)
    is_sankantsu(parsed_hand, yaku_counter, huuro)
    is_sanankou(parsed_hand, yaku_counter)
    is_toitoi(parsed_hand, yaku_counter)
    is_honroutou(tiles_counts, yaku_counter)
    is_sanshoku_doukou(parsed_hand, yaku_counter, huuro)
    is_tanyao(parsed_hand, yaku_counter, huuro)
    is_pinfu(parsed_hand, yaku_counter, huuro)
    is_iipeikou(parsed_hand, yaku_counter, huuro)

    # 排他処理
    resolve_conflicts(yaku_counter, yakumann)
    if yakumann.get_count() == 0 and condition is not None:
        judge_condition_yaku(parsed_hand, yaku_counter, condition)

    # 役満あれば役満のみ返す、そうでなければ通常役を返す
    if yakumann.get_count() > 0:
        return yakumann.get_yakus()
    else:
        return yaku_counter.get_yakus()

def wind_to_tile(wind_str: str) -> str:
    mapping = {
        "east": "z1",
        "south": "z2",
        "west": "z3",
        "north": "z4"
    }
    return mapping.get(wind_str, "z1")

def judge_condition_yaku(parsed_hand, yaku_counter, condition: Condition):
    # 自風・場風タイルの変換
    seat_wind_tile = wind_to_tile(condition.seat_wind)
    prevalent_wind_tile = wind_to_tile(condition.prevalent_wind)
    
    # リーチ関連
    if condition.is_double_riichi:
        if "リーチ" in yaku_counter.get_yakus():
            yaku_counter.remove_yaku("リーチ")
        yaku_counter.add_yaku("ダブルリーチ", 2)
    elif condition.is_riichi:
        yaku_counter.add_yaku("リーチ", 1)
    
    if condition.is_ippatsu:
        yaku_counter.add_yaku("一発", 1)
    if condition.is_rinshan:
        yaku_counter.add_yaku("嶺上開花", 1)
    if condition.is_chankan:
        yaku_counter.add_yaku("槍槓", 1)
    if condition.is_haitei:
        yaku_counter.add_yaku("海底摸月", 1)
    if condition.is_houtei:
        yaku_counter.add_yaku("河底撈魚", 1)
    if condition.is_tenho:
        yaku_counter.add_yaku("天和", 1)
    if condition.is_tsumo:
        yaku_counter.add_yaku("ツモ", 1)
    
    for meld in parsed_hand.get("mentsu", []):
        if meld["type"] in ("kotsu", "kan"):
            tile_idx = meld["tiles"][0]
            tile_str = NUMERIC_TO_TILE[tile_idx]
            if tile_str.startswith("z"):
                if tile_str == seat_wind_tile:
                    yaku_counter.add_yaku("自風牌", 1)
                if tile_str == prevalent_wind_tile:
                    yaku_counter.add_yaku("場風牌", 1)
                if tile_str in ("z5", "z6", "z7"):
                    yaku_counter.add_yaku("三元牌", 1)