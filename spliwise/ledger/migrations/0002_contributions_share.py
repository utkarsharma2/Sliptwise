# Generated by Django 3.2.4 on 2021-06-12 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributions',
            name='share',
            field=models.IntegerField(default=0),
        ),
    ]
