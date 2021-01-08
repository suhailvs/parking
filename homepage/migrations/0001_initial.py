# Generated by Django 3.1.5 on 2021-01-08 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Weeks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromtime', models.PositiveIntegerField()),
                ('totime', models.PositiveIntegerField()),
                ('totalspaces', models.PositiveIntegerField()),
                ('fee', models.PositiveIntegerField(help_text='Parking Fee per hour')),
                ('pic', models.ImageField(blank=True, upload_to='images/', verbose_name='Parking Photos')),
                ('lat', models.CharField(max_length=20)),
                ('lng', models.CharField(max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(help_text="Provide name of location or business, and pertinent details (e.g. use unmarked parking space only, use space with sign marked 'Private' located at end of alley, park off pavement, etc.)", max_length=140)),
                ('status', models.BooleanField(default=True, help_text='Uncheck to temporarily deactivate listing')),
                ('streetaddress', models.CharField(max_length=200)),
                ('days', models.ManyToManyField(help_text=None, to='homepage.Weeks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('park_date', models.DateTimeField()),
                ('duration', models.PositiveIntegerField(default=1)),
                ('paid', models.BooleanField(default=False)),
                ('invoiceid', models.CharField(blank=True, max_length=100)),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.parking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
