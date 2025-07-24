from django.conf import settings
from rest_framework.filters import BaseFilterBackend
from app.core.constants import ModelGrantPermissions


class BasePremissionFilterBackend(BaseFilterBackend):
    """
    Custom filter backend to handle permissions based on user profile and group.
    * User must have a user profile.
    * User Profile must have a base company.
    * Applied to models defined in settings.PERMISSION_MODELS.
    * The model must have a base_company or base_branches field.
    * User must belong to a group.
    * Superuser has accessed to all model.
    """

    def filter_queryset(self, request, queryset, view):
        _model = view.model
        model_name = _model.__name__.lower()

        # Check models permissions
        if model_name not in settings.PERMISSION_MODELS:
            return queryset

        # Grant access to all objects for superusers
        if request.user.is_superuser:
            return queryset

        try:
            # Check user profile and groups
            _user_profile = request.user.user_profile
            _group = request.user.groups
            if not _user_profile or not _user_profile.base_company or not _group:
                queryset = queryset.none()

            # Filter based on granted privacy permissions
            if _group.is_group_company:
                queryset = self.permission_group_company_filter(
                    queryset, _model, model_name, _user_profile
                )

            elif _group.is_company:
                queryset = self.permission_company_filter(
                    queryset, _model, model_name, _user_profile
                )

            elif _group.is_branch:
                queryset = self.permission_branch_filter(
                    queryset, _model, model_name, _user_profile
                )

            else:
                queryset = queryset.none()

        except Exception as e:
            print(f"Error in BasePremissionFilterBackend: {e}")
            queryset = queryset.none()

        return queryset

    def permission_branch_filter(self, queryset, _model, model_name, _user_profile):
        _base_branch_pks = _user_profile.base_branches.all().values_list(
            "pk", flat=True
        )
        if model_name == ModelGrantPermissions.BASE_BRANCH:
            queryset = queryset.filter(id__in=_base_branch_pks)
        elif hasattr(_model, "base_branches"):
            queryset = queryset.filter(base_branches__in=_base_branch_pks)
        else:
            queryset = queryset.none()

        return queryset

    def permission_company_filter(self, queryset, _model, model_name, _user_profile):
        _base_company_pk = _user_profile.base_company.pk
        if model_name == ModelGrantPermissions.BASE_COMPANY:
            queryset = queryset.filter(id=_base_company_pk)
        elif hasattr(_model, "base_company"):
            print(_base_company_pk, "base_company_id")
            queryset = queryset.filter(base_company=_base_company_pk)
        elif hasattr(_model, "base_branches"):
            queryset = queryset.filter(base_branches__base_company=_base_company_pk)
        else:
            queryset = queryset.none()

        return queryset

    def permission_group_company_filter(
        self, queryset, _model, model_name, _user_profile
    ):
        _base_group_company_pk = _user_profile.base_company.base_group_company.pk
        if model_name == ModelGrantPermissions.BASE_GROUP_COMPANY:
            queryset = queryset.filter(id=_base_group_company_pk)
        elif hasattr(_model, "base_group_company"):
            queryset = queryset.filter(base_group_company=_base_group_company_pk)
        elif hasattr(_model, "base_company"):
            queryset = queryset.filter(
                base_company__base_group_company=_base_group_company_pk
            )
        elif hasattr(_model, "base_branches"):
            queryset = queryset.filter(
                base_branches__base_company__base_group_company=_base_group_company_pk
            )
        else:
            queryset = queryset.none()

        return queryset


class CustomBaseFilterBackend(BaseFilterBackend):
    """ "
    Custom filter backend to handle filtering based on query parameters.
    * Filters queryset based on request query parameters."""

    def filter_queryset(self, request, queryset, view):
        filters = {}
        for param, value in request.query_params.items():
            if param in ("page", "paging", "page_size", "ordering", "format", "search"):
                continue

            if param.endswith("__in") or param.endswith("__range"):
                filters[param] = value.split(",")
            elif param.endswith("__isnull") or value.lower() in (
                "true",
                "false",
            ):
                filters[param] = value.lower() == "true"
            else:
                filters[param] = value

        try:
            queryset = queryset.filter(**filters)
        except Exception:
            pass

        return queryset
