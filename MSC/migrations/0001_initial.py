

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_tsumo', models.BooleanField(default=False, verbose_name='ツモ')),
                ('is_riichi', models.BooleanField(default=False, verbose_name='リーチ')),
                ('is_double_riichi', models.BooleanField(default=False, verbose_name='ダブルリーチ')),
                ('is_ippatsu', models.BooleanField(default=False, verbose_name='一発')),
                ('is_rinshan', models.BooleanField(default=False, verbose_name='嶺上開花')),
                ('is_chankan', models.BooleanField(default=False, verbose_name='槍槓')),
                ('is_haitei', models.BooleanField(default=False, verbose_name='海底')),
                ('is_houtei', models.BooleanField(default=False, verbose_name='河底')),
                ('is_tenho', models.BooleanField(default=False, verbose_name='天和')),
                ('is_chiho', models.BooleanField(default=False, verbose_name='地和')),
                ('seat_wind', models.CharField(choices=[('east', '東'), ('south', '南'), ('west', '西'), ('north', '北')], default='east', max_length=5, verbose_name='自風')),
                ('prevalent_wind', models.CharField(choices=[('east', '東'), ('south', '南'), ('west', '西'), ('north', '北')], default='east', max_length=5, verbose_name='場風')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hand_pai', models.JSONField(verbose_name='手牌')),
                ('winning_pai', models.CharField(max_length=3, verbose_name='和了牌')),
                ('is_huuro', models.BooleanField(default=False, verbose_name='副露あり')),
                ('huuro', models.JSONField(default=list, verbose_name='副露の内容')),
                ('dora_pai', models.JSONField(default=list, verbose_name='ドラ表示牌')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('han', models.IntegerField(verbose_name='翻数')),
                ('fu', models.IntegerField(verbose_name='符数')),
                ('point', models.IntegerField(verbose_name='得点')),
                ('yaku_list', models.JSONField(verbose_name='役一覧')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='エラーメッセージ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
