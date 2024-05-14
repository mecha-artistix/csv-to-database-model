from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1 style='font-size:52px; text-align:center; margin-top:50vh; transform:translateY(-50%)'>Welcome to the Django App!</h1>")
