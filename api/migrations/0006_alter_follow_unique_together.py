# Generated by Django 3.2.3 on 2021-05-31 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_follow_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
    ]
