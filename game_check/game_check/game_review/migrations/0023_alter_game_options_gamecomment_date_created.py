# Generated by Django 4.1.3 on 2022-12-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_review', '0022_alter_game_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('title',)},
        ),
        migrations.AddField(
            model_name='gamecomment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2022-12-10'),
            preserve_default=False,
        ),
    ]