# Generated by Django 2.1.3 on 2019-01-06 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20190106_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
