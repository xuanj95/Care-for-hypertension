# Generated by Django 2.2.6 on 2019-10-04 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0004_auto_20191004_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicators',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicators', to='medical.user'),
        ),
    ]
