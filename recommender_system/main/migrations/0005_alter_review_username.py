# Generated by Django 4.2.5 on 2023-10-04 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_product_description_product_image_product_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser', to_field='username'),
        ),
    ]