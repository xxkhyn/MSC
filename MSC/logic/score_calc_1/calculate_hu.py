from MSC.models import Condition
import math
def calculate_fu(parsed_hand, condition):
    is_tsumo = condition.is_tsumo
    is_closed = not parsed_hand.huuro
    melds = parsed_hand.huuro
    pair_tile = parsed_hand.pair_tile  # ← 安全な構造にすべき
    wait_type = detect_wait_type(parsed_hand.tiles, parsed_hand.winning_tile)

    player_wind = condition.convert_wind(condition.seat_wind)
    round_wind = condition.convert_wind(condition.prevalent_wind)

    # 副底符
    fu = 20 if is_tsumo or not is_closed else 30

    # 雀頭が役牌
    if pair_tile in [player_wind, round_wind, 'z5', 'z6', 'z7']:
        fu += 2

    # 面子の符
    for meld in melds:
        t = meld['type']
        tile = meld['tile']
        closed = meld.get('closed', True)
        is_yakuhai = tile.startswith('z')
        is_terminal = tile[1] in ['1', '9']
        is_special = is_yakuhai or is_terminal

        if t == 'chi':
            continue  # 順子は符なし
        elif t == 'pon':
            if is_special:
                fu += 8 if closed else 4
            else:
                fu += 4 if closed else 2
        elif t == 'kan':
            if is_special:
                fu += 32 if closed else 16
            else:
                fu += 16 if closed else 8

    # 待ち形
    if wait_type in ['tanki', 'kanchan', 'penchan']:
        fu += 2

    # 門前ツモボーナス
    if is_tsumo and is_closed:
        fu += 2

    # 切り上げ
    fu = math.ceil(fu / 10) * 10
    return fu
