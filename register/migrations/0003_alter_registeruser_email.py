# Generated by Django 4.2.7 on 2023-11-02 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_alter_registeruser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='email',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
