# Generated by Django 3.1.3 on 2020-11-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='data_date',
            field=models.CharField(default=20200401, max_length=30, verbose_name='データ作成日時'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='detailed_industries_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='詳細業種コード'),
        ),
        migrations.AlterField(
            model_name='company',
            name='industries_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='業種コード'),
        ),
        migrations.AlterField(
            model_name='company',
            name='scale_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='規模コード'),
        ),
        migrations.AlterField(
            model_name='company',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rawprices',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]