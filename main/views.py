from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views import View


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("courses:all"))
        return render(request, "pages/home.html", {
            "website_title": "Home"
        })
