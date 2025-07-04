"""手牌、和了り牌から符計算"""
from MSC.models import Condition
import math

def calculate_fu(parsed_hand, condition):
    """ConditionモデルとParsedHandオブジェクトを元に符数を計算する"""

    is_tsumo = condition.is_tsumo
    is_closed = not parsed_hand.huuro  # 副露なし＝門前
    melds = parsed_hand.huuro  # [{'type': 'pon', 'tile': '9m', 'closed': True}, ...]
    pair_tile = parsed_hand.tiles[-2]  # 便宜的に最後から2枚目を雀頭とする（解析ロジック次第で修正）
    wait_type = detect_wait_type(parsed_hand.tiles, parsed_hand.winning_tile)  # 待ち形の判定関数（仮定）
    player_wind = seat_wind(condition.seat_wind)
    round_wind = convert_wind(condition.prevalent_wind)

    # 🔸 副底符（基本符）
    if is_tsumo:
        fu = 20
    elif not is_closed:
        fu = 20
    else:
        fu = 30

    # 🔸 雀頭（役牌）
    yaku_tiles = [player_wind, round_wind, 'z5', 'z6', 'z7']  # 自風、場風、白發中
    if pair_tile in yaku_tiles:
        fu += 2

    # 🔸 面子
    for meld in melds:
        t = meld['type']
        tile = meld['tile']
        closed = meld.get('closed', True)
        is_yakuhai = tile.startswith('z')
        is_terminal = tile[1] in ['1', '9']
        is_special = is_yakuhai or is_terminal

        if t == 'pon':
            fu += 8 if is_special and closed else 4 if is_special else 4 if closed else 2
        elif t == 'kan':
            fu += 32 if is_special and closed else 16 if is_special else 16 if closed else 8

    # 🔸 待ち形（仮で単騎とカンチャン）
    if wait_type in ['tanki', 'kanchan', 'penchan']:#ひびきまち
        fu += 2

    # 🔸 門前ツモボーナス
    if is_tsumo and is_closed:
        fu += 2

    # 🔸 切り上げ
    fu = math.ceil(fu / 10) * 10
    return fu
