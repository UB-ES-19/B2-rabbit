# Generated by Django 2.2.5 on 2019-11-30 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rabbit', '0010_auto_20191130_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='value',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribing', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscribing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='rabbit.Warren'),
        ),
    ]
