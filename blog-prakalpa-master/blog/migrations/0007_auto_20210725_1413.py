# Generated by Django 3.2.3 on 2021-07-25 08:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210723_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 25, 8, 43, 58, 59827, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 25, 8, 43, 58, 59827, tzinfo=utc)),
        ),
    ]
