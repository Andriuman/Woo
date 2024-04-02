from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .Woo_Script import ejecutar_script

@csrf_exempt  # Deshabilita la verificación de CSRF para esta vista específica
def IntegrarScript(request):
    if request.method == "POST":
        ejecutar_script()
        return HttpResponse("Script ejecutado para POST.")
    else:
        # Podrías manejar otros métodos HTTP aquí, como GET, si fuera necesario
        return HttpResponse("Este método HTTP no está permitido.", status=405)
