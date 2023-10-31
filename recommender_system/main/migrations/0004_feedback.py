# Generated by Django 4.2.5 on 2023-10-31 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_customuser_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='How satisfied are you with your shopping experience?')),
                ('easy_to_navigate', models.BooleanField(verbose_name='Did you find the website easy to navigate?')),
                ('additional_categories', models.TextField(blank=True, verbose_name='What products or categories would you like to see more of on our website?')),
                ('information_found', models.BooleanField(verbose_name='Were you able to find the information you were looking for?')),
                ('comments', models.TextField(blank=True, verbose_name='Any additional comments or suggestions for improvement?')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]