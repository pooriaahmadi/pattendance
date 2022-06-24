from django.conf import settings


def main(request):
    return {
        "DEBUG": settings.DEBUG,
        "WEBSITE_NAME": "Pattendance"
    }
