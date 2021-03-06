# Generated by Django 2.1.3 on 2019-01-07 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_auto_20190106_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='denialreason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='firstapproval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='firstapproval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='application',
            name='secondapproval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='secondapproval', to=settings.AUTH_USER_MODEL),
        ),
    ]
