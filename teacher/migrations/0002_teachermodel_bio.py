# Generated by Django 4.2.11 on 2024-09-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachermodel',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
