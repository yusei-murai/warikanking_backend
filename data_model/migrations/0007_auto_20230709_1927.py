# Generated by Django 3.2.7 on 2023-07-09 19:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_model', '0006_alter_user_user_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='確定'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_identifier',
            field=models.CharField(default=uuid.UUID('f8c8ffbc-7960-40ae-8391-4cc0249fed65'), max_length=255, unique=True, verbose_name='ユーザID'),
        ),
    ]
