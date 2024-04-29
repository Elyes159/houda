import json
from django.http import JsonResponse
from django.shortcuts import render
from flask import redirect
from myapp.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



#### render functions #######

from django.shortcuts import render

from myapp.utils import token_response
from myapp.models import *

def create_account_view(request):
    return render(request, 'myapp/create_account.html')
@csrf_exempt
def login_view(request):
    return render(request, 'myapp/login.html')

def dashbord_view(request, token):
    token = Token.objects.filter(token = token).first()
    if token : 
        return render(request, 'myapp/posts.html')
    

def creation_posts(request) : 
    return render(request,'myapp/recommendation.html')

def creation_transport(request) : 
    return render(request,'myapp/transport.html')



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


from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import json
from rest_framework.permissions import AllowAny


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny]) 
def login_user(request):
    print("mochkol")
    if request.method =='POST' :
        print("mochkol")         
        email = request.data.get('email')
        password = request.data.get('password')
        print("mochkol")
        if email:
            user = User.objects.filter(email=email).first()
        
            password1 = user.password if user else None
        else:
            return JsonResponse({'error': 'data missing'}, status=400)

        if user :
            if password == password1:
                return token_response(user)
                
            else :
                return JsonResponse({'response':'mdpincorrecte'},status = 400)
        else:
            return JsonResponse({'error': 'incorrect password'}, status=400)
    
    


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_post(request,  type_post):
    if request.method == "POST":
            if type_post == 'evenementclub':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                intitule = request.data.get("intitule")
                description = request.data.get("description")
                lieu = request.data.get("lieu")
                contactinfo = request.data.get("contactinfo")
                club = request.data.get("club")
                stage = EvenementClub.objects.create(
                    type=type,
                    image=image_file,
                    intitule = intitule,
                    description = description,
                    lieu = lieu,
                    contactinfo=contactinfo,
                    club = club,
                    
                )
                stage.save()
            elif type_post == 'evenementsociale':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                intitule = request.data.get("intitule")
                description = request.data.get("description")
                lieu = request.data.get("lieu")
                contactinfo = request.data.get("contactinfo")
                prix = request.data.get("prix")
                
                stage = EvenementSociale.objects.create(
                    type=type,
                    image=image_file,
                    intitule = intitule,
                    description = description,
                    lieu = lieu,
                    contactinfo=contactinfo,
                    prix = prix,
                    
                )
                stage.save()
            elif type_post == 'stage':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                societe = request.data.get("societe")
                duree = request.data.get("duree")
                sujet = request.data.get("sujet")
                contactinfo = request.data.get("contactinfo")
                spécialité = request.data.get("spécialité")
                typeStg = request.data.get("typeStg")
                stage = Stage.objects.create(
                    type=type,
                    image=image_file,
                    societe=societe,
                    duree=duree,
                    sujet=sujet,
                    contactinfo=contactinfo,
                    spécialité=spécialité,
                    typeStg=typeStg
                )
                stage.save()
                
            elif type_post == 'logement':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                localisation = request.data.get("localisation")
                contactinfo = request.data.get("contactinfo")
                description = request.data.get("description")
                stage = Logement.objects.create(
                    type=type,
                    image=image_file,
                    contactinfo=contactinfo,
                    description=description,
                    localisation=localisation
                )
                stage.save()
            elif type_post == 'transport':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                depart = request.data.get("depart")
                destination = request.data.get("destination")
                heure_dep = request.data.get("heure_dep")
                nbre_siéges = request.data.get("nbre_siéges")
                contactinfo = request.data.get("contactinfo")
                stage = Transport.objects.create(
                    type=type,
                    image=image_file,
                    depart=depart,
                    destination=destination,
                    heure_dep = heure_dep,
                    nbre_siéges = nbre_siéges,
                    contactinfo=contactinfo
                )
                stage.save()
            elif type_post == 'recommendation':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                text = request.data.get("text")
                stage = Recommendation.objects.create(
                    type=type,
                    image=image_file,
                    text=text,
                   
                )
                stage.save()
            else:
                return JsonResponse({'error': 'Type de poste non valide'})
            
            return JsonResponse({'success': f'Poste de type {type_post} créé avec succès'})
        
from django.shortcuts import render

from django.shortcuts import render

def get_specific_post_data(post):
  if isinstance(post, Evenement):
    return {
        'intitule': post.intitule,
        'description': post.description,
        'lieu': post.lieu,
        'contactinfo': post.contactinfo,
    }
  elif isinstance(post, EvenementClub):
    return {
        'club': post.club,
        **get_specific_post_data(post)  
    }
  elif isinstance(post, EvenementSociale):
    return {
        'prix': post.prix,
        **get_specific_post_data(post)  
    }
  elif isinstance(post, Stage):
    return {
        'typeStg': post.get_typeStg_display(),  
        'societe': post.societe,
        'duree': post.duree,
        'sujet': post.sujet,
        'spécialité': post.spécialité,
    }
  elif isinstance(post, Logement):
    return {
        'localisation': post.localisation,
        'description': post.description,
    }
  elif isinstance(post, Transport):
    return {
        'depart': post.depart,
        'destination': post.destination,
        'heure_dep': post.heure_dep,
        'nbre_siéges': post.nbre_siéges,
    }
  elif isinstance(post, Recommendation):
    return {
        'text': post.text,
    }
  else:
    return {}  

def all_posts(request):
  post_data = {
      'offres': [],  
      'demandes': [],  
  }

  # Get all Poste objects (base class)
  all_postes = Poste.objects.all()

  for post in all_postes:
    if post.type == Poste.TYPE_CHOICES[0][0]:  
      post_data['offres'].append({
          'id': post.id,
          'image': post.image.url if post.image else None,  
          **get_specific_post_data(post),
      })
    elif post.type == Poste.TYPE_CHOICES[1][0]:  
      post_data['demandes'].append({
          'id': post.id,
          'image': post.image.url if post.image else None,
          'date': post.date,
          **get_specific_post_data(post),
      })

  context = {'post_data': post_data}
  return render(request, 'myapp/posts.html', context)


        


