# Generated by Django 4.1.3 on 2022-12-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_review', '0005_gamecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamecomment',
            name='content',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]