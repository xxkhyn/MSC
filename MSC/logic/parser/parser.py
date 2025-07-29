import copy
from MSC.logic.parser import parse_def
from types import SimpleNamespace
def analyze_hand_model(hand_obj):
    hand_numeric = parse_def.tile_strs_to_indices(hand_obj)
    melds = parse_def.parse_huuro_to_melds(hand_obj)
    agari_patterns = parse_def.can_form_agari_numeric(hand_obj)
    mentsu_to_dict = parse_def.mentsu_to_dict 
    if not agari_patterns:
        return {
            "agari_patterns": [],
            "melds": melds,
            "melds_descriptions": [],
            "error_message": "和了形が作れません。牌が不足しているか、面子が作れません。"
        }

    first_pattern = agari_patterns[0][0]

    melds_descriptions = [parse_def.describe_mentsu(mentsu_to_dict(m)) for m in first_pattern]

    return {
        "agari_patterns": agari_patterns,
        "melds": melds,
        "melds_descriptions": melds_descriptions,
        "error_message": ""
    }
#test用データ
hand_obj = SimpleNamespace(
    hand_pai=["s1","s2","s3","p1","p1","p1","s7","s8","s9","z1","z1","z2","z2"],
    winning_pai="z2",
    huuro=[],
    dora_pai=[]
)

result = analyze_hand_model(hand_obj)


print("Agari Patterns:", result["agari_patterns"])
print("Melds:", result["melds"])
print("Melds Descriptions:", result["melds_descriptions"])
print("Error Message:", result["error_message"])