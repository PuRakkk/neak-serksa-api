from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('app.auth_user.urls')),
] 