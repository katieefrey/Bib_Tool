# Generated by Django 3.0.4 on 2021-02-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibtool', '0019_auto_20210126_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='newarticle',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
