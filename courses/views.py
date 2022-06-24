import uuid

from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from django.views import View
from django.utils import timezone
from django.conf import settings
from .models import Course, EditForm
from classes.models import Class
from users.models import User
from attendance.models import Attendance
import datetime


def join_lists(lists):
    output = []
    for l in lists:
        output.extend(l)
    return output


class All(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:home"))

        time = datetime.datetime.now(tz=timezone.get_current_timezone())
        courses = list(filter(lambda x: x.end_time >= time, Course.objects.filter(active=True)))
        associated_classes = []
        for c in Class.objects.all():
            for user in c.associated_users.all():
                if request.user == user:
                    associated_classes.append(c)
        not_submitted_courses = []
        for course in courses:
            for associated_class in associated_classes:
                if associated_class in course.classes.all():
                    not_submitted_courses.append(course)

        submitted_courses = []
        attendance = Attendance.objects.filter(user=request.user)
        for not_submitted_course in not_submitted_courses:
            for record in attendance:
                if record.course == not_submitted_course:
                    submitted_courses.append(not_submitted_course)
                    not_submitted_courses.remove(not_submitted_course)

        return render(request, "pages/courses_all.html", {
            "website_title": "Courses",
            'not_submitted_courses': not_submitted_courses,
            'submitted_courses': submitted_courses,
            'attendance': attendance
        })


class AllAdmin(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("courses:all"))

        courses = Course.objects.all()
        return render(request, "pages/courses_all_manage.html", {
            "website_title": "Manage - Courses",
            'courses': courses
        })


class Delete(View):
    def post(self, request, id):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("courses:all"))

        course = Course.objects.filter(id=id)
        if not course.exists():
            return HttpResponseRedirect(reverse("courses:all_manage"))

        course = course.first()
        attendance = Attendance.objects.filter(course=course)
        attendance.delete()
        course.delete()

        return HttpResponseRedirect(reverse("courses:all_manage"))


class Edit(View):
    def get(self, request, id):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("courses:all"))

        course = Course.objects.filter(id=id)
        if not course.exists():
            return HttpResponseRedirect(reverse("courses:all_manage"))

        course = course.first()
        course.code = uuid.uuid4().hex.upper()[0:6]
        course.save()
        attendance = Attendance.objects.filter(course=course)
        classes = course.classes.all()
        associated_users = join_lists([c.associated_users.all() for c in classes])
        return render(request, "pages/course_edit.html", {
            "website_title": course.title,
            "course": course,
            "attendance": list(map(lambda x: x.user, attendance)),
            "associated_users": User.objects.all() if len(associated_users) == 0 else associated_users,
            'course_opts': Course._meta,
            'attendance_opts': Attendance._meta
        })

    def post(self, request, id):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("courses:all"))

        course = Course.objects.filter(id=id)
        if not course.exists():
            return HttpResponseRedirect(reverse("courses:all_manage"))

        course = course.first()
        title = request.POST.get("title", None)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)
        if not title or not start_time or not end_time:
            return HttpResponse("Invalid data")

        course.title = title
        course.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        course.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        course.save()

        attendance = Attendance.objects.filter(course=course)
        classes = course.classes.all()
        associated_users = join_lists([c.associated_users.all() for c in classes])
        return render(request, "pages/course_edit.html", {
            "website_title": course.title,
            "course": course,
            "attendance": list(map(lambda x: x.user, attendance)),
            "associated_users": User.objects.all() if len(associated_users) == 0 else associated_users,
            'course_opts': Course._meta,
            'attendance_opts': Attendance._meta
        })


class CourseView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:home"))

        course = Course.objects.filter(id=id)
        if not course.exists():
            return HttpResponseRedirect(reverse("courses:all"))

        course = course.first()
        if not course.active:
            return HttpResponseRedirect(reverse("courses:all"))

        attendance = Attendance.objects.filter(user=request.user, course=course)
        attendance = attendance.first() if attendance.exists() else None

        return render(request, "pages/course_view.html", {
            "website_title": course.title,
            "course": course,
            "attendance": attendance
        })

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:home"))
        code = request.POST.get("code")
        if not code:
            return HttpResponseRedirect(reverse("courses:all"))

        course = Course.objects.filter(id=id)
        if not course.exists():
            return HttpResponseRedirect(reverse("courses:all"))
        course = course.first()
        if not course.active:
            return HttpResponseRedirect(reverse("courses:all"))
        if not course.code == code:
            return render(request, "pages/course_view.html", {
                "website_title": course.title,
                "course": course,
                "error": True,
                "details": "I'm sorry, buddy. Try again pls <3"
            })

        time = datetime.datetime.now(tz=timezone.get_current_timezone())
        if time < course.start_time:
            return render(request, "pages/course_view.html", {
                "website_title": course.title,
                "course": course,
                "error": True,
                "details": "The classes has not been started yet."
            })

        classes = course.classes.all()
        associated_users = join_lists([c.associated_users.all() for c in classes])
        if not request.user in associated_users:
            return render(request, "pages/course_view.html", {
                "website_title": course.title,
                "course": course,
                "error": True,
                "details": "This isn't your class."
            })

        attendance = Attendance.objects.create(user=request.user, course=course)
        attendance.save()
        return render(request, "pages/course_view.html", {
            "website_title": course.title,
            "course": course,
            "attendance": attendance
        })


class Submit(View):
    def get(self, request, id, code):
        if not request.user.is_authenticated:
            hostname = 'http://localhost:8000' if settings.DEBUG else 'https://pattendance.pooria.tech'
            google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
            redirect_uri = reverse("users:google_callback")
            scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
            params = {
                'response_type': 'code',
                'client_id': '154280617493-rgn5mgluofrr9ea18l2iunavner30a40.apps.googleusercontent.com',
                'redirect_uri': f"{hostname}{redirect_uri}",
                'prompt': 'select_account',
                'access_type': 'offline',
                'scope': scope
            }
            string_params = "?"
            for key, value in params.items():
                string_params += f"{key}={value}&"
            response = HttpResponseRedirect(f"{google_auth_url}{string_params}")
            response.set_cookie('requested_course', f"{id}:{code}")
            return response

        if not code:
            return HttpResponseRedirect(reverse("courses:all"))

        course = Course.objects.filter(id=id)
        if not course.exists():
            return HttpResponseRedirect(reverse("courses:all"))
        course = course.first()
        if not course.active:
            return HttpResponseRedirect(reverse("courses:all"))
        if not course.code == code:
            return render(request, "pages/course_view.html", {
                "website_title": course.title,
                "course": course,
                "error": True,
                "details": "I'm sorry, buddy. Try again pls <3"
            })

        time = datetime.datetime.now(tz=timezone.get_current_timezone())
        if time < course.start_time:
            return render(request, "pages/course_view.html", {
                "website_title": course.title,
                "course": course,
                "error": True,
                "details": "The classes has not been started yet."
            })

        classes = course.classes.all()
        associated_users = join_lists([c.associated_users.all() for c in classes])
        if not request.user in associated_users:
            return render(request, "pages/course_view.html", {
                "website_title": course.title,
                "course": course,
                "error": True,
                "details": "This isn't your class."
            })

        attendance = Attendance.objects.create(user=request.user, course=course)
        attendance.save()
        return render(request, "pages/course_view.html", {
            "website_title": course.title,
            "course": course,
            "attendance": attendance
        })
