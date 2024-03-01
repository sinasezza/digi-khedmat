from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import authentication as rest_authentications
from rest_framework import permissions as rest_permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status as rest_status
from .. import models, permissions


@api_view(http_method_names=["DELETE",])
@authentication_classes((rest_authentications.SessionAuthentication,))
@permission_classes((permissions.IsRoomMember,))
def room_delete_api(request: HttpRequest, name: str) -> Response:
    if request.method == "DELETE":
        room = get_object_or_404(models.Thread, name=name)
        room.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------

@api_view(http_method_names=('POST',))
@authentication_classes([rest_authentications.SessionAuthentication,])
@permission_classes([permissions.IsRoomMember,])
def room_report_api(request: HttpRequest, name: str) -> Response:
    if request.method == "POST":
        room = get_object_or_404(models.Thread, name=name)
        message = request.data.get('message')
        report = models.Report.objects.create(thread=room, reporter=request.user, message=message)
        
        return Response(data={"message": "این مورد گزارش شد.",}, status=rest_status.HTTP_201_CREATED)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)
