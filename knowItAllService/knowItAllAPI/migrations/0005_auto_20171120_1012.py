# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 10:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowItAllAPI', '0004_auto_20171120_0500'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('userID', 'pollID')]),
        ),
    ]
