# Generated by Django 2.2.24 on 2023-07-02 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestiary', '0034_auto_20230630_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='com2us_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='dungeon',
            name='com2us_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='enemy',
            name='com2us_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='gameitem',
            name='category',
            field=models.IntegerField(choices=[(1, 'Monster'), (6, 'Currency'), (9, 'Summoning Scroll'), (10, 'Booster'), (11, 'Essence'), (12, 'Monster Piece'), (19, 'Guild Monster Piece'), (25, 'Rainbowmon'), (27, 'Rune Craft'), (29, 'Craft Material'), (30, 'Secret Dungeon'), (61, 'Enhancing Monster'), (73, 'Artifact'), (75, 'Artifact Craft Material'), (82, 'Unknown Category')], db_index=True, help_text='Typically corresponds to `item_master_id` field'),
        ),
        migrations.AlterField(
            model_name='gameitem',
            name='com2us_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='monster',
            name='com2us_id',
            field=models.IntegerField(blank=True, db_index=True, help_text='ID given in game data files', null=True),
        ),
        migrations.AlterField(
            model_name='scalingstat',
            name='com2us_desc',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='com2us_id',
            field=models.IntegerField(blank=True, db_index=True, help_text='ID given in game data files', null=True),
        ),
        migrations.AlterField(
            model_name='skilleffect',
            name='type',
            field=models.IntegerField(choices=[(-1, 'Debuff'), (0, 'Neutral'), (1, 'Buff')], db_index=True, default=0),
        ),
    ]
