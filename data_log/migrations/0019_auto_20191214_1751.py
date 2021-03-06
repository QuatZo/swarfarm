# Generated by Django 2.2.9.dev20191214052109 on 2019-12-15 01:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_log', '0018_auto_20190909_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='craftrunelog',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='craftrunelog',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='craftrunelog',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='craftrunelog',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
        migrations.AddField(
            model_name='dungeonrunedrop',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='dungeonrunedrop',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='dungeonrunedrop',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='dungeonrunedrop',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
        migrations.AddField(
            model_name='magicboxcraftrunedrop',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='magicboxcraftrunedrop',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='magicboxcraftrunedrop',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='magicboxcraftrunedrop',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
        migrations.AddField(
            model_name='riftdungeonrunedrop',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='riftdungeonrunedrop',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='riftdungeonrunedrop',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='riftdungeonrunedrop',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
        migrations.AddField(
            model_name='shoprefreshrunedrop',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='shoprefreshrunedrop',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='shoprefreshrunedrop',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='shoprefreshrunedrop',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
        migrations.AddField(
            model_name='wishlogrunedrop',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='wishlogrunedrop',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='wishlogrunedrop',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='wishlogrunedrop',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
        migrations.AddField(
            model_name='worldbosslogrunedrop',
            name='has_gem',
            field=models.BooleanField(default=False, help_text='Has had an enchant gem applied'),
        ),
        migrations.AddField(
            model_name='worldbosslogrunedrop',
            name='has_grind',
            field=models.IntegerField(default=0, help_text='Number of grindstones applied'),
        ),
        migrations.AddField(
            model_name='worldbosslogrunedrop',
            name='substats_enchanted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(blank=True, default=False), default=list, size=4),
        ),
        migrations.AddField(
            model_name='worldbosslogrunedrop',
            name='substats_grind_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), default=list, size=4),
        ),
    ]
