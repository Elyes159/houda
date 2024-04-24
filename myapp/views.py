import json
from django.http import JsonResponse
from django.shortcuts import render
from myapp.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



#### render functions #######

from django.shortcuts import render

def create_account_view(request):
    return render(request, 'myapp/create_account.html')


#### render functions #######

@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_account(request):
    if request.method == 'POST':
        try:
            data = request.data

            nom = data.get('nom')
            prenom = data.get('nom')

            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')

            print(f"Received data - Email: {email}, Phone: {phone}, Password: {password}")

            if email and phone and password:
                print(f"Trying to find Otp for phone: {phone}")
               
                User.objects.create(nom=nom, prenom=prenom, email=email, phone=phone, password=password)
                # otp_obj.delete()
                return HttpResponse("account created successfully")
            else:
                error_message = "Invalid data provided. "
                if not email:
                    error_message += "Email is required. "
                if not phone:
                    error_message += "Phone is required. "
                if not password:
                    error_message += "Password is required. "
                if not nom:
                    error_message += "nom is required. "
                if not prenom:
                    error_message += "prenom is required. "
                print(f"Error message: {error_message.strip()}")

                return HttpResponse(error_message.strip(), status=400)

        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format in the request body", status=400)

        except Exception as e:
            print(f"Error: {str(e)}")
            return HttpResponse("An error occurred while processing the request", status=500)

    return HttpResponse("Invalid request method", status=405)
