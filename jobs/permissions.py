from rest_framework import permissions


class IsJobOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

# ===========================================================

class IsResumeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user