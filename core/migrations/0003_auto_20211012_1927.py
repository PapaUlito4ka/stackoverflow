# Generated by Django 3.0.8 on 2021-10-12 19:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211012_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 19, 27, 53, 803211, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 19, 27, 53, 802218, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 19, 27, 53, 801233, tzinfo=utc)),
        ),
    ]
