import os

SECRET_KEY = "12345"

DATABASES = {"default": {
 "ENGINE": "django.db.backends.sqlite3",
 "NAME": "tests/integration/testserver/db.sqlite3"
}}

STATIC_URL = "/static/"

ROOT_URLCONF = "tests.integration.testserver.urls"

INSTALLED_APPS = [
 "graphene_django",
 "tests.integration.testserver",
]

GRAPHENE = {
 "SCHEMA": "tests.integration.testserver.schema.schema"
}
