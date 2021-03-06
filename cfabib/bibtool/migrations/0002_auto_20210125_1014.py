# Generated by Django 3.0.4 on 2021-01-25 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bibtool', '0001_initial'),
        ('bibmanage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='adminbibgroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Bibgroup'),
        ),
        migrations.AddField(
            model_name='article',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Batch'),
        ),
        migrations.AddField(
            model_name='article',
            name='guess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibtool.Guess'),
        ),
        migrations.AddField(
            model_name='article',
            name='inst',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibtool.Affil'),
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibtool.Status'),
        ),
        migrations.AddField(
            model_name='affil',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
