# Generated by Django 4.0.4 on 2022-05-29 18:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_alter_course_end_time_alter_course_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='associated_users',
            field=models.ManyToManyField(null=True, related_name='students', to=settings.AUTH_USER_MODEL),
        ),
    ]
