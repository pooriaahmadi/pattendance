# Generated by Django 4.0.4 on 2022-05-31 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_course_associated_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=191, null=True),
        ),
    ]
