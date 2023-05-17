# Generated by Django 3.0.8 on 2022-05-05 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bibmanage', '0004_auto_20200317_1505'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bibcode', models.CharField(max_length=19, unique=True)),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('query', models.CharField(blank=True, max_length=100, null=True)),
                ('affils', models.TextField(blank=True, null=True)),
                ('authnum', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('adminbibgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Bibgroup')),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Batch')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('affil', models.TextField(blank=True, null=True)),
                ('query', models.CharField(blank=True, max_length=100, null=True)),
                ('autoclass', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('edited', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('adminbibgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Bibgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guess', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibtool.Author')),
                ('bibcode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibtool.Article')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bibcode', models.CharField(max_length=19, unique=True)),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('authnum', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('adminbibgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Bibgroup')),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibmanage.Batch')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='bibcode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibtool.NewArticle'),
        ),
        migrations.AddField(
            model_name='author',
            name='guess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibtool.Guess'),
        ),
        migrations.AddField(
            model_name='author',
            name='inst',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibtool.Affil'),
        ),
        migrations.AddField(
            model_name='author',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibtool.Status'),
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
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('bibcode', 'name', 'affil', 'adminbibgroup')},
        ),
    ]
