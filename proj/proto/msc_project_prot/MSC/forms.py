from django import forms
from .models import Condition
import json

class ConditionForm(forms.Form):
    is_tsumo = forms.BooleanField(required=False, label="ツモ")
    is_riichi = forms.BooleanField(required=False, label="リーチ")
    is_double_riichi = forms.BooleanField(required=False, label="ダブルリーチ")
    is_ippatsu = forms.BooleanField(required=False, label="一発")
    is_rinshan = forms.BooleanField(required=False, label="嶺上開花")
    is_chankan = forms.BooleanField(required=False, label="槍槓")
    is_haitei = forms.BooleanField(required=False, label="海底")
    is_houtei = forms.BooleanField(required=False, label="河底")
    is_tenho = forms.BooleanField(required=False, label="天和")
    is_chiho = forms.BooleanField(required=False, label="地和")

    seat_wind = forms.ChoiceField(choices=Condition.WIND_CHOICES, label="自風")
    prevalent_wind = forms.ChoiceField(choices=Condition.WIND_CHOICES, label="場風")

    def clean(self):
        cleaned_data = super().clean()
        # 例：天和はツモ必須
        if cleaned_data.get("is_tenho") and not cleaned_data.get("is_tsumo"):
            raise forms.ValidationError("天和を選択した場合、ツモも選択してください。")
        return cleaned_data

class HandForm(forms.Form):
    hand_pai = forms.CharField(
        label="手牌（13枚）",
        help_text="カンマ区切りで入力（例： 1m, 1m, 1m, 2p, 3p, ...）"
    )

    winning_pai = forms.CharField(label="和了牌（例： 5p）")

    is_huuro = forms.BooleanField(required=False, label="副露あり")

    dora_pai = forms.CharField(
        required=False,
        label="ドラ表示牌",
        help_text="カンマ区切り（例： 5p, 2m）"
    )

    huuro = forms.CharField(
        required=False,
        label="副露の詳細（JSON形式）",
        help_text='例： [{"tyep": "chi", "tiles": ["3m", "4m", "5m"]}, {"type": "kan", "tiles": ["7s", "7s", "7s", "7s"], "open": true}]'
    )

    def clean_hand_pai(self):
        raw = self.cleaned_data['hand_pai']
        pai_list = [p.strip() for p in raw.split(',')]
        if len(pai_list) != 13:
            raise forms.ValidationError("手牌は13枚で入力してください。")
        return pai_list

    def clean_dora_pai(self):
        raw = self.cleaned_data.get('dora_pai', '')
        return [p.strip() for p in raw.split(',')] if raw else []

    def clean_huuro(self):
        raw = self.cleaned_data.get('huuro', '')
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, list):
                raise ValueError
            return parsed
        except Exception:
            raise forms.ValidationError("副露の内容は正しいJSON配列で入力してください。")
        