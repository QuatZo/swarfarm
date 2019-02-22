# Generated by Django 2.1.7 on 2019-02-22 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestiary', '0003_auto_20190221_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={'ordering': ('dungeon', 'difficulty', 'floor')},
        ),
        migrations.AlterField(
            model_name='dungeon',
            name='category',
            field=models.IntegerField(blank=True, choices=[(0, 'Scenario'), (1, 'Caiross Dungeon'), (2, 'Tower of Ascension'), (3, 'Rift Raid'), (4, 'Rift Beast'), (5, 'Hall of Heroes'), (99, 'Other')], null=True),
        ),
    ]
