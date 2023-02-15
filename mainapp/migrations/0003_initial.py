# Generated by Django 4.0.4 on 2022-04-20 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0002_delete_buyer_remove_product_brand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('phone', models.CharField(max_length=14)),
                ('address1', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('address2', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('address3', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('pin', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('pic', models.FileField(blank=True, default=None, null=True, upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='Maincategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('phone', models.CharField(max_length=14)),
                ('address1', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('address2', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('address3', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('pin', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('pic', models.FileField(blank=True, default=None, null=True, upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('baseprice', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('finalprice', models.IntegerField()),
                ('size', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('stock', models.CharField(default='In stock', max_length=20)),
                ('pic1', models.ImageField(upload_to='', verbose_name='image1')),
                ('pic2', models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='image2')),
                ('pic3', models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='image3')),
                ('pic4', models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='image4')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.brand')),
                ('maincategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.maincategory')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcategory')),
            ],
        ),
    ]
