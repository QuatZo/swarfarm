# Generated by Django 2.2.24 on 2023-07-16 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herders', '0034_auto_20230716_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='last_update',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]