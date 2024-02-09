from rest_framework import permissions


class IsNotificationOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        print(f"objs recipient is {obj.recipient} and request user is {request.user}")

        return obj.recipient == request.user