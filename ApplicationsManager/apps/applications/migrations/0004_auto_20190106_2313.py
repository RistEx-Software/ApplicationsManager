# Generated by Django 2.1.3 on 2019-01-06 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0003_application_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='decisiontime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='denialreason',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='firstapproval',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='firstapproval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='secondapproval',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='secondapproval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('0', 'Pending'), ('1', 'Denied'), ('2', 'Approved')], default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='application',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
