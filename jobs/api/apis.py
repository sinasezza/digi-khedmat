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
@permission_classes((permissions.IsResumeOwner,))
def resume_delete_api(request: HttpRequest, id: str) -> Response:
    if request.method == "DELETE":
        resume = get_object_or_404(models.Resume, id=id)
        resume.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------

@api_view(http_method_names=["DELETE",])
@authentication_classes((rest_authentications.SessionAuthentication,))
@permission_classes((permissions.IsResumeOwner,))
def resume_file_delete_api(request: HttpRequest, id: str) -> Response:
    if request.method == "DELETE":
        resume = get_object_or_404(models.ResumeFile, id=id)
        resume.delete()
        return Response(status=rest_status.HTTP_204_NO_CONTENT)
    else:
        return Response(data={"message": "BAD REQUEST!"}, status=rest_status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([rest_permissions.AllowAny])
def job_fetch_views_api(request: HttpRequest, job_slug: str):
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    return Response(data={'views': job.views}, status=rest_status.HTTP_200_OK)


# ------------------------------------------------------------------------------------

@api_view(http_method_names=["DELETE",])
@authentication_classes((rest_authentications.SessionAuthentication,))
@permission_classes((permissions.IsJobOwnerOrReadOnly,))
def job_delete_api(request: HttpRequest, job_slug: str) -> Response:
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    job.delete()
    return Response(status=rest_status.HTTP_204_NO_CONTENT)