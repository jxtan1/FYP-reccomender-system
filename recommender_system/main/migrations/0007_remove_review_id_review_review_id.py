# Generated by Django 4.2.5 on 2023-10-05 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_delete_reviewer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='id',
        ),
        migrations.AddField(
            model_name='review',
            name='review_id',
            field=models.AutoField(default=-1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
