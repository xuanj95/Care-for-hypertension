# Generated by Django 2.2.6 on 2019-10-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0002_auto_20191004_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicators',
            name='bloodOxygenation',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='diastolicBloodPressure',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='heartRate',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='indicators',
            name='systolicBloodPressure',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
