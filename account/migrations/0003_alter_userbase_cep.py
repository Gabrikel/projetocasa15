# Generated by Django 3.2.5 on 2021-07-28 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userbase_cpf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='cep',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
