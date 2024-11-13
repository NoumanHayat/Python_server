# views.py
from django.http import HttpResponse

def my_new_view(request):
    return HttpResponse("Hello, this is my new URL!")
