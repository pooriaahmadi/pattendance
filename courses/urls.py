from django.urls import path
from .views import *

app_name = "courses"

urlpatterns = [
    path("all", All.as_view(), name="all"),
    path("all/manage", AllAdmin.as_view(), name="all_manage"),
    path("<int:id>/view", CourseView.as_view(), name="course_view"),
    path("<int:id>/edit", Edit.as_view(), name="edit"),
    path("<int:id>/delete", Delete.as_view(), name="delete")
]
