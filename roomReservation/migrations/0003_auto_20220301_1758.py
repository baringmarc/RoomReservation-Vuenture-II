# Generated by Django 3.2.6 on 2022-03-01 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomReservation', '0002_auto_20220301_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conferenceroom',
            name='fee',
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='afternoonFee',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='eveningFee',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='morningFee',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Fee',
        ),
    ]
