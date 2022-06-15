from django.db import models
from pattendance.settings import AUTH_USER_MODEL


class Class(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    associated_users = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name="students_in_a_group",
        blank=True
    )

    def __str__(self):
        return f"{self.title} | {len(list(self.associated_users.all()))} students"
