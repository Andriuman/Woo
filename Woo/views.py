from django.shortcuts import render

from django.http import HttpResponse
from .Woo_Script import ejecutar_script

def IntegrarScript(request):
    ejecutar_script()
    return HttpResponse("Script ejecutado.")
