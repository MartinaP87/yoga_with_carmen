# Generated by Django 3.2.16 on 2022-12-27 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='annotation',
            field=models.CharField(default='Remember...', max_length=300),
        ),
    ]