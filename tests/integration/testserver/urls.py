from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
 path("", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]
