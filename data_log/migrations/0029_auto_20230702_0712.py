# Generated by Django 2.2.24 on 2023-07-02 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_log', '0028_auto_20230630_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='craftrunelog',
            name='craft_level',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Mid'), (3, 'High'), (4, 'Ancient'), (5, 'Legend')]),
        ),
        migrations.AlterField(
            model_name='craftrunelog',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='dungeonartifactdrop',
            name='archetype',
            field=models.CharField(blank=True, choices=[('attack', 'Attack'), ('hp', 'HP'), ('support', 'Support'), ('defense', 'Defense'), ('material', 'Material')], db_index=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dungeonartifactdrop',
            name='element',
            field=models.CharField(blank=True, choices=[('fire', 'Fire'), ('wind', 'Wind'), ('water', 'Water'), ('light', 'Light'), ('dark', 'Dark')], db_index=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='dungeonartifactdrop',
            name='slot',
            field=models.IntegerField(choices=[(1, 'Element'), (2, 'Archetype')], db_index=True),
        ),
        migrations.AlterField(
            model_name='dungeonlog',
            name='success',
            field=models.NullBooleanField(db_index=True, help_text='Null indicates that run was not completed'),
        ),
        migrations.AlterField(
            model_name='dungeonrunedrop',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='magicboxcraftingreport',
            name='box_type',
            field=models.IntegerField(choices=[(8, 'Unknown Magic Box'), (9, 'Mystical Magic Box'), (12, 'Legendary Magic Box')], db_index=True),
        ),
        migrations.AlterField(
            model_name='magicboxcraftrunedrop',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='riftdungeonlog',
            name='grade',
            field=models.IntegerField(choices=[(1, 'F'), (2, 'D'), (3, 'C'), (4, 'B-'), (5, 'B'), (6, 'B+'), (7, 'A-'), (8, 'A'), (9, 'A+'), (10, 'S'), (11, 'SS'), (12, 'SSS')], db_index=True),
        ),
        migrations.AlterField(
            model_name='riftdungeonlog',
            name='success',
            field=models.BooleanField(db_index=True),
        ),
        migrations.AlterField(
            model_name='riftdungeonrunedrop',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='riftraidlog',
            name='success',
            field=models.NullBooleanField(db_index=True, help_text='Null indicates that run was not completed'),
        ),
        migrations.AlterField(
            model_name='runecraftingreport',
            name='craft_level',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Mid'), (3, 'High'), (4, 'Ancient'), (5, 'Legend')], db_index=True),
        ),
        migrations.AlterField(
            model_name='shoprefreshrunedrop',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='wishlogrunedrop',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='worldbosslogrunedrop',
            name='slot',
            field=models.IntegerField(db_index=True),
        ),
    ]
