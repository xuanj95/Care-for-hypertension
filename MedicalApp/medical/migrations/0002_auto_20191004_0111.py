# Generated by Django 2.2.6 on 2019-10-03 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicators',
            name='bloodOxygenation',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='createDate',
            field=models.DateField(auto_created=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='diastolicBloodPressure',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='heartRate',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='systolicBloodPressure',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]