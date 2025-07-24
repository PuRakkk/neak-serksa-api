from app.core.views import CoreCreateViewSet
from app.auth_user.models import User
from app.auth_user.serializers import UserSerializer
from django.db import transaction
from rest_framework.response import Response
from app.services.mail_sender import send_single_email
from django.contrib.auth import authenticate
import random


class CreateUserView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        pw = data.get("password")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.set_password(pw)
        serializer.save()
        return Response(
            {
                "message": "Successful Signin",
            },
            status=201,
        )


class UserLoginView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        user = authenticate(request, email=data.get("email"), password=data.get("password"))
        if not user:
            return Response({"message": "invalid_email_or_password"}, status=400)

        if not user.is_verify:
            otp = random.randint(100000, 999999)
            try:
                send_single_email(
                    recipient=data.get("email"),
                    subject="Welcome to Nek Seksa!",
                    body=f"Here is your OPT: {otp}",
                )
                user.otp = otp
                user.save()
                return Response({"message": "verify_otp"}, status=200)
            
            except Exception as e:
                return Response({"error": "invalid_email"}, status=500)
        return Response({"message": "login_success"}, status=200)


class VerifyOTPView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data.get("email")).first()

        if user.otp != data.get("otp"):
            return Response({
                "message": "incorrect_otp"
            }, status=400)
        
        user.is_verify = True
        user.save()
        return Response({
            "message": "redirect_to_login"
        }, status=200)
        
