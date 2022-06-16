from django.db import models
from django.forms import ModelForm, DateTimeInput
from django.contrib import admin
from pattendance.settings import AUTH_USER_MODEL
from classes.models import Class


class Course(models.Model):
    teacher = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False, blank=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    classes = models.ManyToManyField(
        Class,
        blank=True
    )
    code = models.CharField(
        max_length=191,
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=True
    )

    @admin.display
    def classes_display(self):
        classes = self.classes.all()
        if not len(classes):
            return 'All students'
        return ', '.join([c.title for c in classes])

    def __str__(self):
        return f"{self.title}"


class EditForm(ModelForm):
    class Meta:
        model = Course
        fields = ["title", "start_time", "end_time"]
        widgets = {
            'start_time': DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_time': DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
        }
