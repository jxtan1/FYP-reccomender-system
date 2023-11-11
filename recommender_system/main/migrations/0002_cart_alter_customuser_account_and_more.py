# Generated by Django 4.2.5 on 2023-11-10 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='account',
            field=models.CharField(choices=[('B', 'Buyer'), ('S', 'Seller'), ('A', 'Admin')], max_length=1),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='SellerFeedback',
            fields=[
                ('feedback_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='How satisfied are you with your experience as a seller on our platform?')),
                ('easy_to_sell', models.BooleanField(verbose_name='Was it easy to list your products on our platform?')),
                ('fee_structure', models.BooleanField(verbose_name='Were you satisfied with the payment process and fee structure?')),
                ('customer_support', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='How would you rate the support provided to sellers by our customer support team?')),
                ('comments', models.TextField(blank=True, verbose_name='Any additional comments or suggestions for improvement?')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFeedback',
            fields=[
                ('feedback_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='How satisfied are you with your shopping experience?')),
                ('easy_to_navigate', models.BooleanField(verbose_name='Did you find the website easy to navigate?')),
                ('additional_categories', models.TextField(blank=True, verbose_name='What products or categories would you like to see more of on our website?')),
                ('information_found', models.BooleanField(verbose_name='Were you able to find the information you were looking for?')),
                ('recommendation_relevance', models.BooleanField(verbose_name='Do you find the recommended products relevant to your interest?')),
                ('recommendation_accuracy_rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='How would you rate our product recommendation accuracy?')),
                ('comments', models.TextField(blank=True, verbose_name='Any additional comments or suggestions for improvement?')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='main.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]