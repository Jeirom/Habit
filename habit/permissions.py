from rest_framework import permissions

class IsOwnerOrPublic(permissions.BasePermission):
    """
    Позволяет редактировать объект только его владельцу,
    а также позволяет просматривать объекты, если они публичные.
    """

    def has_object_permission(self, request, view, obj):
        # Позволяем редактировать, если пользователь является владельцем
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.owner == request.user
        return obj.owner == request.user