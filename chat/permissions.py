from rest_framework import permissions


class IsRoomMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return ((obj.user1 == request.user) or (obj.user1 == request.user))