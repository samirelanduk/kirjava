from graphene_django.views import GraphQLView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
 path("", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
