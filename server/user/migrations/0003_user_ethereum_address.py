# Generated by Django 4.2.2 on 2024-08-07 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_username_user_first_name_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ethereum_address',
            field=models.CharField(default='Default_Ehtereum_Address', max_length=256),
        ),
    ]
