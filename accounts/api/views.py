from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import authentication as rest_authentications
from rest_framework import permissions as rest_permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status as rest_status
from .. import models, permissions

def handle_api_response(success_message: str, error_message: str, status_code: int):
    def decorator(func):
        def wrapper(request: HttpRequest, id: str) -> Response:
            try:
                return func(request, id)
            except models.Notification.DoesNotExist:
                return Response(data={"message": "NOT FOUND"}, status=rest_status.HTTP_404_NOT_FOUND)
            except:
                return Response(data={"message": "INTERNAL SERVER ERROR"}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrapper

    return decorator

# --------------------------------------------------------------------------------

@api_view(http_method_names=('DELETE',))
@authentication_classes([rest_authentications.SessionAuthentication,])
@permission_classes([permissions.IsNotificationOwnerOrReadOnly,])
@handle_api_response("Notification deleted successfully", "Error deleting notification", rest_status.HTTP_204_NO_CONTENT)
def delete_notification_api(request: HttpRequest, id: str) -> Response:
    if request.method == "DELETE":
        notification = models.Notification.objects.get(id=id)
        notification.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------

@api_view(http_method_names=("PATCH",))
@authentication_classes([rest_authentications.SessionAuthentication,])
@permission_classes([permissions.IsNotificationOwnerOrReadOnly,])
@handle_api_response("Notification marked as read successfully", "Error marking notification as read", rest_status.HTTP_204_NO_CONTENT)
def mark_as_read_api(request: HttpRequest, id: str) -> Response:
    if request.method == "PATCH":
        notification = models.Notification.objects.get(id=id)
        notification.toggle_seen()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------

@api_view(http_method_names=('DELETE',))
@authentication_classes([rest_authentications.SessionAuthentication,])
@permission_classes([permissions.IsNotificationOwnerOrReadOnly,])
@handle_api_response("Favorite Object deleted successfully", "Error deleting notification", rest_status.HTTP_204_NO_CONTENT)
def delete_favorite_api(request: HttpRequest, id: str) -> Response:
    if request.method == "DELETE":
        notification = models.Favorite.objects.get(id=id)
        notification.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------