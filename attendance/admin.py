from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field
from .models import Attendance
from courses.admin import CourseFilter


class AttendanceResource(ModelResource):
    user_full_name = Field(column_name='user_full_name')
    user_email = Field(column_name='user_email')
    course = Field(column_name='course')

    def dehydrate_user_full_name(self, attendance):
        first_name = getattr(attendance.user, "first_name", "unknown")
        last_name = getattr(attendance.user, "last_name", "unknown")
        return f"{first_name} {last_name}"

    def dehydrate_user_email(self, attendance):
        email = getattr(attendance.user, "email", "unknown")
        return email

    def dehydrate_course(self, attendance):
        title = getattr(attendance.course, "title", "unknown")
        return title

    class Meta:
        model = Attendance
        fields = ('user_full_name', 'user_email', 'course', 'timestamp')


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AttendanceResource
    list_display = ('user', 'course', 'timestamp')
    list_filter = ('user', CourseFilter)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'course__title')
