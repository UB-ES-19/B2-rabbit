# Generated by Django 2.2.5 on 2019-11-30 11:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rabbit', '0009_auto_20191130_1124'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('user', 'post', 'comment')},
        ),
    ]