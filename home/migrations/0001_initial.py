# Generated by Django 4.1.6 on 2023-02-06 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FineTunedModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50)),
            ],
        ),
    ]