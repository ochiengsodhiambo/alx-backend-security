from django.shortcuts import render

# Create your views here.
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse

@ratelimit(key='user', rate='10/m', block=True)
def login_authenticated(request):
    return HttpResponse("Authenticated login attempt")

@ratelimit(key='ip', rate='5/m', block=True)
def login_anonymous(request):
    return HttpResponse("Anonymous login attempt")

