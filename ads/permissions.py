from rest_framework import permissions


class IsStuffAdvertisingOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.stuff_advertising.owner == request.user

