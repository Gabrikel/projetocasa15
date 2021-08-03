# Generated by Django 3.2.5 on 2021-08-03 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='product.product'),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
