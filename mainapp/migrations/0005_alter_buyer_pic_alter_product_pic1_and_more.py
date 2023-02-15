# Generated by Django 4.0.4 on 2022-05-17 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_maincategory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='pic',
            field=models.FileField(blank=True, default='noimage.jpg', null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic1',
            field=models.ImageField(blank=True, default='noimage.jpg', null=True, upload_to='', verbose_name='image1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic2',
            field=models.ImageField(blank=True, default='noimage.jpg', null=True, upload_to='', verbose_name='image2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic3',
            field=models.ImageField(blank=True, default='noimage.jpg', null=True, upload_to='', verbose_name='image3'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic4',
            field=models.ImageField(blank=True, default='noimage.jpg', null=True, upload_to='', verbose_name='image4'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='pic',
            field=models.FileField(blank=True, default='noimage.jpg', null=True, upload_to='image'),
        ),
    ]
