# Generated by Django 3.2.7 on 2023-04-02 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='イベント名')),
                ('total', models.IntegerField(default=0, verbose_name='合計金額')),
                ('number_people', models.IntegerField(default=0, verbose_name='合計金額')),
            ],
        ),
    ]