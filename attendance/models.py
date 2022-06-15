from django.db import models
from courses.models import Course
import datetime

from pattendance.settings import AUTH_USER_MODEL


class Attendance(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} | {self.course.title} {self.course.id} | {self.timestamp}"
