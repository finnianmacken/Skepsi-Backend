# Generated by Django 3.1.7 on 2021-07-15 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skepsi_app', '0031_auto_20210715_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='figure',
            name='name',
            field=models.CharField(default='', max_length=2500),
        ),
    ]