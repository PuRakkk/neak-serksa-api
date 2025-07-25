from django.urls import path, include
from rest_framework import routers
from app.auth_user.views import CreateUserView, UserLoginView, VerifyOTPView, GetUserInfoView, UpdateUserProfile

router = routers.SimpleRouter(trailing_slash=False)
# router.register("user", CreateUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register", CreateUserView.as_view()),
    path("login", UserLoginView.as_view()),
    path("otp", VerifyOTPView.as_view()),
    path("get_user/<str:email>", GetUserInfoView.as_view()),
    path("update/<int:id>", UpdateUserProfile.as_view()),
]