# Generated by Django 3.2.6 on 2022-03-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomReservation', '0004_reservation_timeslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
