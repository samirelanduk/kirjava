from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", FileUploadGraphQLView.as_view()),
]
