# Generated by Django 2.2.24 on 2023-07-02 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herders', '0032_auto_20230702_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monsterinstance',
            name='com2us_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
