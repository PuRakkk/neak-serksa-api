from rest_framework import permissions


class IsPermissionAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        model = view.queryset.model
        model_name = model._meta.model_name

        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm(f"view_{model_name}")
        elif request.method == "POST":
            return request.user.has_perm(f"add_{model_name}")
        elif request.method in ["PUT", "PATCH"]:
            return request.user.has_perm(f"change_{model_name}")
        elif request.method == "DELETE":
            return request.user.has_perm(f"delete_{model_name}")
        else:
            return False
