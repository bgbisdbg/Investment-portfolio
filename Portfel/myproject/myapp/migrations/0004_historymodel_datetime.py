# Generated by Django 3.2.12 on 2024-02-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_briefcasemodel_historymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='historymodel',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
