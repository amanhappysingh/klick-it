# Generated by Django 4.0.4 on 2022-08-09 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_rename_paymentststus_checkout_paymentstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newslatter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=80)),
            ],
        ),
    ]
