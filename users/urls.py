from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path("google/landing", GoogleLanding.as_view(), name="google_landing"),
    path("google/callback", GoogleCallback.as_view(), name="google_callback")
]
