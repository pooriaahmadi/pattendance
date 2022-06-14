from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.conf import settings
from .models import User
import requests


class GoogleLanding(View):
    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("courses:all"))
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
        return HttpResponseRedirect(f"{google_auth_url}{string_params}")


class GoogleCallback(View):
    def get(self, request):
        code = request.GET.get("code", None)
        error = request.GET.get("error", None)
        if error:
            return HttpResponse(str(error))

        hostname = 'http://localhost:8000' if settings.DEBUG else 'https://pattendance.pooria.tech'

        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            'code': code,
            'client_id': '154280617493-rgn5mgluofrr9ea18l2iunavner30a40.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': f'{hostname}/users/google/callback',
            'grant_type': 'authorization_code'
        }
        response = requests.post("https://oauth2.googleapis.com/token", data=data)
        if not response.ok:
            return HttpResponse(response.text)

        access_token = response.json()["access_token"]
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params={'access_token': access_token}
        )
        data = response.json()
        user = User.objects.filter(email=data["email"])
        if user.exists():
            user = user[0]
            user.first_name = data["given_name"]
            user.last_name = data["family_name"]
            user.avatar = data["picture"]
            user.save()
        else:
            user = User.objects.create_user(username=data["email"].split("@")[0],
                                            email=data["email"],
                                            password=data["sub"],
                                            )
            user.first_name = data["given_name"]
            user.last_name = data["family_name"]
            user.avatar = data["picture"]
            user.save()

        login(request, user)
        return HttpResponseRedirect(reverse("courses:all"))
