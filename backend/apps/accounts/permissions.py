from rest_framework.permissions import BasePermission


class IsAdminOrGerente(BasePermission):
    """Permite acceso solo a administradores y gerentes."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin_or_gerente
        )


class IsAdmin(BasePermission):
    """Permite acceso solo a administradores."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )
