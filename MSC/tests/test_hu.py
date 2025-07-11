from types import SimpleNamespace
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
from MSC.logic.object.melds import TILE_TO_INDEX

# テスト用のhand_instance作成
test_hand_instance = SimpleNamespace(
    is_tsumo=True,
    is_huuro=False,
    winning_pai="m2"  # 実際に和了した牌（TILE_TO_INDEXで数値に変換される）
)

# テスト用のcondition_instance作成（役牌：自風 東、場風 南）
test_condition_instance = SimpleNamespace(
    seat_wind="east",
    prevalent_wind="south"
)

# agari_pattern（順子、刻子、雀頭などの構成）
# 例: [m2,m3,m4], [p1,p1,p1], [z1,z1,z1], [z2,z2,z2], 雀頭[z3,z3]
mentsu_list = [
    [TILE_TO_INDEX["m2"], TILE_TO_INDEX["m3"], TILE_TO_INDEX["m4"]],  # 順子
    [TILE_TO_INDEX["p1"]] * 3,  # 中張牌の暗刻
    [TILE_TO_INDEX["z1"]] * 3,  # 自風（東）役牌
    [TILE_TO_INDEX["z2"]] * 3   # 場風（南）役牌
]
head = [TILE_TO_INDEX["z3"], TILE_TO_INDEX["z3"]]  # 白（z3）雀頭

agari_pattern = (mentsu_list, head)

# 実行
fu_result = calculate_fu(test_hand_instance, test_condition_instance, agari_pattern)
print(f"符計算結果: {fu_result}")
