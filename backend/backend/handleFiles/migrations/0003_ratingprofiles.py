# Generated by Django 5.0.6 on 2024-05-15 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleFiles', '0002_actions_attributes_rates_ratingplans_routes_stats_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingProfiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tenant', models.CharField(max_length=250)),
                ('Category', models.CharField(max_length=250)),
                ('Subject', models.CharField(max_length=250)),
                ('ActivationTime', models.DateField()),
                ('RatingPlanId', models.CharField(max_length=250)),
                ('RatesFallbackSubject', models.CharField(max_length=250)),
            ],
        ),
    ]