# Generated by Django 4.2.5 on 2023-10-30 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='account',
            field=models.CharField(choices=[('B', 'Buyer'), ('S', 'Seller'), ('A', 'Admin')], max_length=1),
        ),
    ]
