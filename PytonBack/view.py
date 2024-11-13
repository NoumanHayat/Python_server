# views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


def welcome_view(request):
    return HttpResponse("Welcome to the new page!")


#@csrf_exempt
  # Disable CSRF protection for testing purposes; remove in production or secure with proper tokens
def echo_data(request):
    if request.method == "GET":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            return JsonResponse(data)  # Send the same data back as a JSON response
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import io
import contextlib

@csrf_exempt  # Disable CSRF for testing; use CSRF tokens in production
def execute_code(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            code = data.get("code")
            
            if not code:
                return JsonResponse({"error": "No code provided"}, status=400)
            
            # Capture the output of the executed code
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec(code)  # Dangerous: Only use if input is trusted

            # Retrieve the output and return it in the response
            result = output.getvalue()
            return JsonResponse({"result": result})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
