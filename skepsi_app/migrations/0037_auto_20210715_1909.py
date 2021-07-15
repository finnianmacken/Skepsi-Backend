# Generated by Django 3.1.7 on 2021-07-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skepsi_app', '0036_auto_20210715_1907'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='score',
            name='A score is valid between 1 and 10 (inclusive)',
        ),
        migrations.AddConstraint(
            model_name='score',
            constraint=models.CheckConstraint(check=models.Q(score__gte=1), name='A score is valid between 1 and 10 (inclusive)'),
        ),
    ]
