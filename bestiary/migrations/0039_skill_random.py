# Generated by Django 2.2.28 on 2023-12-09 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestiary', '0038_auto_20231204_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='random',
            field=models.BooleanField(default=False, help_text='Skill attacks randomly'),
        ),
    ]
