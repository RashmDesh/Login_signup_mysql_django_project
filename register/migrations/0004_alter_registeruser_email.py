# Generated by Django 4.2.7 on 2023-11-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_registeruser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='email',
            field=models.EmailField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
