# views.py
from django.db import connection
from django.http import JsonResponse

def ping(request):
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "healthy", "message": "pong"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "unhealthy", "message": str(e)}, status=503)