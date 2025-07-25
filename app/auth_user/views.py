from app.core.views import CoreCreateViewSet, CoreRetrieveViewSet
from app.auth_user.models import User
from app.auth_user.serializers import UserSerializer
from django.db import transaction
from rest_framework.response import Response
from app.services.mail_sender import send_single_email
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import random
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


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
        user = authenticate(
            request, email=data.get("email"), password=data.get("password")
        )
        if not user:
            return Response({"message": "invalid_email_or_password"}, status=404)

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

        token = self.get_jwt_token(user)
        token_response = self.get_response_token_jwt(token)

        return token_response

    def get_response_token_jwt(self, token):
        response = Response()
        response.set_cookie(
            key="refreshToken",
            value=token["refresh_token"],
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
            domain=settings.JWT_COOKIE_DOMAIN,
        )
        response.set_cookie(
            key="accessToken",
            value=token["access_token"],
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
            domain=settings.JWT_COOKIE_DOMAIN,
        )

        response.data = {
            "token": {
                "access_token": token["access_token"],
                "refresh_token": token["refresh_token"],
            },
            "message": "login_success",
        }
        return response

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        token = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

        return token


class VerifyOTPView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data.get("email")).first()

        if user.otp != data.get("otp"):
            return Response({"message": "incorrect_otp"}, status=404)

        user.is_verify = True
        user.save()
        return Response({"message": "redirect_to_login"}, status=200)


class GetUserInfoView(CoreRetrieveViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    lookup_field = "email"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
