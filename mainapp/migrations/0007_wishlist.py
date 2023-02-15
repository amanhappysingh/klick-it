# Generated by Django 4.0.4 on 2022-08-01 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_product_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]
