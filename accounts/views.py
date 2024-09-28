from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from . import models
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from .models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login,logout
from .serializer import RegisterSerializer,LoginSerializer,UserProfileSerializer,UserPasswordChangeSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer, UserImageSerializer
# Create your views here.
class UserRegisationView(CreateAPIView):
    queryset=models.User.objects.all()
    serializer_class=RegisterSerializer
    def post(self, request, format=None):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://online-school-project.onrender.com/api/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('registation_confirm_email.html', {'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            success="success"
            return Response({"registrationStatus": success},status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def activate(request, uid64, token):
    print(uid64,token)
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        print(user)
        user.save()
        return redirect('verified_success')
    else:
        return redirect('verified_unsuccess')
    


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)

                role = 'user'
                if user.is_superuser or user.is_staff:
                    role = 'admin'
                elif user.is_teacher:
                    role = 'teacher'
                elif not user.is_active:
                    return Response({
                        'error': "Your account is not active. Please activate your account before logging in."
                    }, status=status.HTTP_403_FORBIDDEN)

                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'role': role
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': {"non_field_errors": ["Email or Password is not valid"]}}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileApiView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserProfileSerializer

class ProfileImageChangeView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=UserImageSerializer
    def post(self, request):
        user=request.user
        serializer=UserImageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordChangeApiView(APIView):
    serializer_class =UserPasswordChangeSerializer
    permission_classes=[IsAuthenticated]
    def post(self, request,format=None):
        serializer=UserPasswordChangeSerializer(data=request.data, context={"user":request.user})
        if serializer.is_valid():
            return Response({"msg":"Successfully Change Your Password"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailApiView(APIView):
    serializer_class=SendPasswordResetEmailSerializer
    def post(self, request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg":"Password Reset Link Send. Please Check Your Email"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetApiView(APIView):
    serializer_class=UserPasswordResetSerializer
    def post(self,request,uid, token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data, context={"uid":uid,"token":token})
        if serializer.is_valid():
            return Response({"msg":"Password Reset Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            logout(request)
            return Response({"msg": "Successfully logged out"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)


# add success message
def successful(request):
    return render(request, 'successful.html')

# add unsuccessful message
def unsuccessful(request):
    return render(request, 'unsuccessful.html')
