from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, ContractSerializer
from rest_framework.response import Response
from .models import User, Contract, HotelijerProfile, Room, Reservation
from django.core.mail import EmailMessage
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator 
from django.core.validators import EmailValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from django.db import transaction
import jwt, datetime
import threading


# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send(fail_silently=True)  
       
class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        for user in users:
            print(f"Email: {user.email}, User Type: {user.user_type}, is_active {user.is_active}, is_superuser {user.is_superuser} ")
        return Response({"message":"users"})

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
        
        if not user:
            return Response({"message":"User not found"})
        
        if not user.is_active:
            raise AuthenticationFailed("Account not activated!")
                
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        payload = {
            "id" : user.id,
            "role": user.user_type,
            "username": user.name,
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
    
class RequestPasswordResetEmail(APIView):
    def get(self, request):
        pass
    
    def post(self, request):
        
        email = request.data.get('resetEmail')
        
        email_validator = EmailValidator()
        if not email_validator(email):
            return Response({"message":"Email is not valid!"})
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"message":"Email is not valid!"})
        
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
        token = PasswordResetTokenGenerator().make_token(user)
        domain = get_current_site(request).domain
        link = reverse('reset-user-password', kwargs={'uidb64':uidb64, 'token':token}) 
        activate_url='http://'+domain+link
        
        response = Response()
        resetPasswordInformaton = {'token':token, 'uidb64':uidb64,'link_opened': False}
        
        response.data = resetPasswordInformaton
        
        email_body = 'Hello, use this link to reset your password.\n'+ activate_url
        email_subject='Password reset email'
        email = EmailMessage(
            email_subject,
            email_body,
            "djox17@gmail.com",
            [email],
        )
        # email.send(fail_silently=False)
        EmailThread(email).start()
        print("response: ", response.data)
        return response

class CompletePasswordReset(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                response = Response()
                response.set_cookie(key='email-link', value=True)
                return response
            else:
                return Response({"message": "Invalid token."}, status=400)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"message": "Invalid user ID."}, status=400)
            
    def post(self,request, uidb64, token):
        newPassword = request.data.get('newPassword')
        confirmNewPassword =  request.data.get("confirmNewPassword")

        if not (newPassword == confirmNewPassword):
            return Response({'message':'password must match!'})
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))   
            user=User.objects.get(pk=user_id)
            user.set_password(newPassword)
            user.save()
            return Response({"message":"Password successfully reseted"})
        except Exception as identifier:
            return Response({"message":"Something went wrong!"})
        
class EditProfile(APIView):
    def post(self, request, uidb64):
        try:
            user_id = force_bytes(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.name=request.data['name']
            user.save()
            return Response({"message":"successfull edited profile"})
        except Exception as identifier:
            return Response({"message":'Something went wrong with editing profile'})

class CreateContract(APIView):
    def post(self, request):
        print("contract: ", request.data)
        request.data['status'] = 'pending'
        
        serializer = ContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.save()
        
        print("contract created", contract)
        return Response({"message":"Successfully created contract"})

class AcceptContract(APIView):
    def post(self, request, contract_id):
        try:
            contract = Contract.objects.get(pk=contract_id)
            contract.status = 'accepted'
            contract.save() 

            return Response({"message": "Successfully accepted contract"})
            
        except Contract.DoesNotExist:
            return Response({"message": "Contract not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class RejectContract(APIView):
    def post(self, request, contract_id):
        try:
            contract = Contract.objects.get(pk=contract_id)
            contract.status = 'rejected'
            contract.save() 

            return Response({"message": "Successfully rejected contract"})
            
        except Contract.DoesNotExist:
            return Response({"message": "Contract not found"}, status=status.HTTP_404_NOT_FOUND)
        
class  GetAllContracts(APIView):
    def get(self, request):
        try:
            contracts = Contract.objects.all()
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        except:
            return  Response({"error":"An error occurred while fetch:"})
        

class GetAllAcceptedContracts(APIView):
    def get(self, request):
        try:
            accepted_contracts = Contract.objects.filter(status='accepted')
            serializer = ContractSerializer(accepted_contracts, many=True)
            data = serializer.data
            
            users = User.objects.all()
            for user in users:
                print(f"Email: {user.email}, User Type: {user.user_type}, is_active {user.is_active}, is_superuser {user.is_superuser}, id: {user.pk} ")

            hotelijer_ids = [contract['hotelijerId'] for contract in data]

            hotelijer_profiles = HotelijerProfile.objects.filter(user_id__in=hotelijer_ids)

            results = [
                {
                    'id': profile.user_id,
                    'name': profile.user.name,
                    'email': profile.user.email,
                    'balance': profile.balance,
                    'contract_id': contract['contractId']
                }
                for profile in hotelijer_profiles
                for contract in data
                if profile.user_id == contract['hotelijerId']
            ]

            return Response(results)
        except Exception as e:
            return Response({"error": f"An error occurred while fetching accepted contracts: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MakeReservation(APIView):
    def post(self, request):
        try:
            room_id = request.data['room_id']
            room = Room.objects.get(id=room_id)

            user = User.objects.get(email=room.hotelijer)
            
            hotelijer_profile = HotelijerProfile.objects.get(user=user)
            
            if room.is_booked:
                return Response({"error": "Room is already booked"}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                reservation = Reservation(room=room)
                reservation.save()

                room.is_booked = True
                room.save()

                hotelijer_profile.balance += room.price
                hotelijer_profile.save()

                return Response({"message": "Reservation created successfully"}, status=status.HTTP_201_CREATED)
        except Room.DoesNotExist:
            return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Hotelijer user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except HotelijerProfile.DoesNotExist:
            return Response({"error": "Hotelijer profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred while making reservation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CancelReservation(APIView):
    def post(self, request):
        try:
            room_id = request.data['room_id']
            room = Room.objects.get(id=room_id)
            
            user = User.objects.get(email=room.hotelijer)

            hotelijer_profile = HotelijerProfile.objects.get(user=user)

            amount = room.price

            if room.is_booked:
                with transaction.atomic():
                    hotelijer_profile.balance -= amount
                    hotelijer_profile.save()

                    room.is_booked = False
                    room.save()

                return Response({"message": "Reservation successfully canceled"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Room is not booked!"}, status=status.HTTP_400_BAD_REQUEST)
        except Room.DoesNotExist:
            return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Hotelijer user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except HotelijerProfile.DoesNotExist:
            return Response({"error": "Hotelijer profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred! {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
