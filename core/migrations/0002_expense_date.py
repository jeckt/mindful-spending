# Generated by Django 2.0.7 on 2018-08-04 23:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
