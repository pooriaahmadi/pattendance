# Generated by Django 4.0.4 on 2022-05-26 15:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField(default=datetime.datetime(2022, 5, 26, 11, 42, 46, 858559))),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
