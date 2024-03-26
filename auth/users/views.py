from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from django.core.mail import EmailMessage
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator 
import jwt, datetime
import threading


# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send(fail_silently=True)  
        

class RegisterView(APIView):
    def post(self, request):
        print("request.data: ", request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Sending verification email
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        token = token_generator.make_token(user)
        activate_url = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
        activation_link = f"http://{domain}{activate_url}"

        email_body = 'Hello ' + user.name +' ,use this link to verify your account.\n'+ activation_link
        print('email_body', email_body)
        email_subject='Activate your account'
        email = EmailMessage(
            email_subject,
            email_body,
            "djox17@gmail.com",
            [user.email],
        )
        EmailThread(email).start()

        return Response(serializer.data)

       
    
    

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        if not user.is_active:
            raise AuthenticationFailed("Account not activated!")
                
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        payload = {
            "id" : user.id,
            "exp":datetime.datetime.utcnow()+ datetime.timedelta(minutes=60),
            "iat":datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, "secret", algorithm="HS256")# Hash-based- Message Authentication Code
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
            "jwt":token
        }
            
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
           
        user = User.objects.filter(id = payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'successfully logged out'
        }
        return response
        
        
class VerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return Response({"message":"Token not found"})

            if user.is_active:
                return Response({"message":"Already used activation link"})
            user.is_active = True
            user.save()

            return Response({"message":"Successfully activated account"})


        except Exception as ex:
            pass

        return Response({"message":"Error!!!"})

