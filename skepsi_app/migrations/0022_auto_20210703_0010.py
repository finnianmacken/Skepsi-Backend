# Generated by Django 3.1.7 on 2021-07-03 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skepsi_app', '0021_auto_20210703_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='paperOrder',
            field=models.IntegerField(default=1, unique=True),
        ),
    ]
