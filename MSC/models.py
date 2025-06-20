from django.db import models

# 条件オブジェクト
class Condition(models.Model):
  """ユーザーが選択する麻雀の状況条件（リーチ、ツモ、チーなど）を保持するモデル"""

  is_tsumo = models.BooleanField(default=False, verbose_name="ツモ")
  is_riichi = models.BooleanField(default=False, verbose_name="リーチ")
  is_double_riichi = models.BooleanField(default=False, verbose_name="ダブルリーチ")
  is_ippatsu = models.BooleanField(default=False, verbose_name="一発")
  is_rinshan = models.BooleanField(default=False, verbose_name="嶺上開花")
  is_chankan = models.BooleanField(default=False, verbose_name="槍槓")
  is_haitei = models.BooleanField(default=False, verbose_name="海底")
  is_houtei = models.BooleanField(default=False, verbose_name="河底")
  is_tenho = models.BooleanField(default=False, verbose_name="天和")
  is_chiho = models.BooleanField(default=False, verbose_name="地和")

  WIND_CHOICES = [
        ('east', '東'),
        ('south', '南'),
        ('west', '西'),
        ('north', '北'),
  ]

  seat_wind = models.CharField(max_length=5, choices=WIND_CHOICES, default='east', verbose_name="自風")
  prevalent_wind = models.CharField(max_length=5, choices=WIND_CHOICES, default='east', verbose_name="場風")

  PLAYER_TYPE_CHOICES = [
    ('parent', '親'),
    ('child', '子'),
  ]

  player_type = models.CharField(
    max_length=6,
    choices=PLAYER_TYPE_CHOICES,
    default='child',
    verbose_name="親 or 子"
  )

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Condition(Riichi={self.is_riichi}, Tsumo={self.is_tsumo})"

# 手牌オブジェクト
class Hand(models.Model):
  """ユーザーが選択した、点数を知りたいユーザー自身の手牌の情報を保存する"""

  # 手牌13枚
  hand_pai = models.JSONField(verbose_name="手牌")

  # 和了牌 
  winning_pai = models.CharField(max_length=3, verbose_name="和了牌") 
 
  
  # 副露をしているかどうか
  is_huuro = models.BooleanField(default=False, verbose_name="副露あり")

  # 副露の詳細
  huuro = models.JSONField(default=list, verbose_name="副露の内容")

  # ドラ表示牌
  dora_pai = models.JSONField(default=list, verbose_name="ドラ表示牌")

  # 作成日時
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Hand({','.join(self.hand_pai)} + {self.winning_pai})"
  
# 点数計算結果オブジェクト
class ScoreResult(models.Model):
    han = models.IntegerField(verbose_name="翻数")
    fu = models.IntegerField(verbose_name="符数")
    point = models.IntegerField(verbose_name="得点")
    yaku_list = models.JSONField(verbose_name="役一覧")
    error_message = models.TextField(blank=True, null=True, verbose_name="エラーメッセージ")
    created_at = models.DateTimeField(auto_now_add=True)

