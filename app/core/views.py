from rest_framework import viewsets
from rest_framework import generics
from app.core.permissions import IsPermissionAccess
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class CustomFilterBackendMixin:
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]


class CoreViewSet(CustomFilterBackendMixin, viewsets.ModelViewSet):
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = "-id"
    permission_classes = [IsAuthenticated, IsPermissionAccess]


class CoreListViewSet(CustomFilterBackendMixin, generics.ListAPIView):
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = "-id"
    permission_classes = [IsAuthenticated, IsPermissionAccess]

    
    
class CoreCreateViewSet(CustomFilterBackendMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsPermissionAccess]



class CoreRetrieveViewSet(CustomFilterBackendMixin, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsPermissionAccess]



class CoreUpdateViewSet(CustomFilterBackendMixin, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsPermissionAccess]


class CoreDeleteViewSet(CustomFilterBackendMixin, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsPermissionAccess]
