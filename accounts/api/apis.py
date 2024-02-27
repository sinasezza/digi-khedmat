from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import authentication as rest_authentications
from rest_framework import permissions as rest_permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status as rest_status
from django.contrib.contenttypes.models import ContentType
from .. import models, permissions, utils

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
@permission_classes([permissions.IsFavoriteOwnerOrReadOnly,])
@handle_api_response("Favorite Object deleted successfully", "Error deleting Favorite Object", rest_status.HTTP_204_NO_CONTENT)
def delete_favorite_api(request: HttpRequest, id: str) -> Response:
    if request.method == "DELETE":
        favorite_obj = models.Favorite.objects.get(id=id)
        favorite_obj.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------

@api_view(http_method_names=('POST',))
@authentication_classes([rest_authentications.SessionAuthentication,])
@permission_classes([permissions.IsFavoriteOwnerOrReadOnly,])
def add_favorite_api(request: HttpRequest) -> Response:
    if request.method == "POST":
        advertisement_id = request.data.get('advertisement_id')
        advertisement_type = request.data.get('advertisement_type')
        
        # Check if the advertisement type is valid
        if advertisement_type not in ['BarterAdvertising', 'StuffAdvertising', 'JobAdvertising']:
            return Response(data={"message": "Invalid advertisement type"}, status=rest_status.HTTP_400_BAD_REQUEST)
        
        # Get the ContentType object for the advertisement type
        content_type = ContentType.objects.get(model=advertisement_type.lower())
        
        try:
            # Create a Favorite object
            favorite = models.Favorite.objects.create(
                owner=request.user,
                advertisement_type=content_type,
                object_id=advertisement_id
            )
            return Response(data={"message": "Favorite Object Created successfully", 'favorite_id': favorite.id,}, status=rest_status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"message": str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------

@api_view(http_method_names=('POST',))
@permission_classes([rest_permissions.AllowAny])
def send_otp_api(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        user = utils.find_phone_number_owner(phone_number)
        
        if user is not None:
            check = utils.check_last_otp(user)
            if check:
                utils.create_otp(phone_number, user)
                return Response(data={"message": "کد تایید برای شما ارسال شد و پس از 2 دقیقه منقضی میشود."}, status=rest_status.HTTP_200_OK)
            else:
                return Response(data={"message": "از ارسال کد قبلی بیش از 2 دقیقه نگذشته است."}, status=rest_status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={"message": "این شماره تلفن در سامانه موجود نیست."}, status=rest_status.HTTP_404_NOT_FOUND)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)