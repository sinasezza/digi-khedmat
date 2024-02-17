from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import authentication as rest_authentications
from rest_framework import permissions as rest_permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status as rest_status
from django.contrib.contenttypes.models import ContentType
from .. import models, permissions


@api_view(http_method_names=('DELETE',))
@authentication_classes([rest_authentications.SessionAuthentication,])
@permission_classes([permissions.IsStuffAdvertisingOwnerOrReadOnly,])
def stuff_image_delete_api(request: HttpRequest, id: int):
    if request.method == "DELETE":
        image = models.StuffImage.objects.get(id=id)
        image.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)


