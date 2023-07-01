# Generated by Django 3.2.7 on 2023-06-30 17:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_model', '0002_alter_friend_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_identifier',
            field=models.CharField(default=uuid.uuid4, max_length=255, null=True, verbose_name='ユーザID'),
        ),
    ]
