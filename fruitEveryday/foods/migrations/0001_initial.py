# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cPrice', models.DecimalField(max_digits=5, decimal_places=2)),
                ('cNum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetailOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dNum', models.IntegerField()),
                ('dPrice', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('oSum', models.DecimalField(max_digits=6, decimal_places=2)),
                ('oIspay', models.BooleanField()),
                ('oTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pName', models.CharField(max_length=50)),
                ('pPrice', models.DecimalField(max_digits=4, decimal_places=2)),
                ('pStock', models.IntegerField()),
                ('pDesc', models.CharField(max_length=1000)),
                ('pDetail', tinymce.models.HTMLField()),
                ('pTime', models.DateTimeField(auto_now_add=True)),
                ('pImg', models.ImageField(upload_to=b'upload/')),
                ('pUnit', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RencentMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rTime', models.DateTimeField(auto_now_add=True)),
                ('rProName', models.ForeignKey(to='foods.ProductInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Sort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sClass', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uName', models.CharField(max_length=20)),
                ('uPwd', models.CharField(max_length=100)),
                ('uEmail', models.EmailField(max_length=254)),
                ('uPhone', models.DecimalField(null=True, max_digits=11, decimal_places=0)),
                ('uAddr', models.CharField(max_length=200, null=True)),
                ('uTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='rencentmap',
            name='rUser',
            field=models.ForeignKey(to='foods.UserInfo'),
        ),
        migrations.AddField(
            model_name='productinfo',
            name='pClass',
            field=models.ForeignKey(to='foods.Sort'),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='oUser',
            field=models.ForeignKey(to='foods.UserInfo'),
        ),
        migrations.AddField(
            model_name='detailorder',
            name='dMain',
            field=models.ForeignKey(to='foods.OrderList'),
        ),
        migrations.AddField(
            model_name='detailorder',
            name='dProduct',
            field=models.ForeignKey(to='foods.ProductInfo'),
        ),
        migrations.AddField(
            model_name='cartlist',
            name='cProduct',
            field=models.ForeignKey(to='foods.ProductInfo'),
        ),
        migrations.AddField(
            model_name='cartlist',
            name='cUser',
            field=models.ForeignKey(to='foods.UserInfo'),
        ),
    ]
