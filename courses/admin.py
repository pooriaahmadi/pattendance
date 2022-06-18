from django.contrib import admin
from courses.models import Course


class CourseFilter(admin.SimpleListFilter):
    title = "course"
    parameter_name = "course"

    def lookups(self, request, model_admin):
        courses = [(c.id, c.title) for c in Course.objects.all()]
        return courses

    def queryset(self, request, queryset):
        if not self.value():
            return queryset.all()
        return queryset.filter(course__id=self.value())


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'classes_display')
    list_filter = ('teacher',)
    filter_horizontal = ('classes',)
    search_fields = ('title',)
