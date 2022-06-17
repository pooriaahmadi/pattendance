from django.db import models
from django.contrib import admin
from pattendance.settings import AUTH_USER_MODEL


class Class(models.Model):
    class Meta:
        verbose_name_plural = "Classes"

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

    @admin.display
    def users(self):
        return len(list(self.associated_users.all()))

    def __str__(self):
        return self.title
