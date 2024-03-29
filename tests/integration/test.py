from contextlib import redirect_stderr
import sys
import os
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "tests.integration.testserver.settings"
)
import json
import django; django.setup()
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.test.utils import override_settings
import kirjava

@override_settings(DEBUG=True)
class KirjavaTests(LiveServerTestCase):

    def test_client(self):
        # Basic
        client = kirjava.Client(self.live_server_url)
        self.assertEqual(
            client.execute("{ name }"),
            {"data": {"name": "The Republic of Heaven"}}
        )

        # With headers
        client.headers["KEY"] = "VALUE"
        self.assertEqual(
            client.execute("{ name headers}"),
            {"data": {
                "name": "The Republic of Heaven",
                "headers": "HTTP_ACCEPT, HTTP_ACCEPT_ENCODING, HTTP_CONNECTION, HTTP_COOKIE, HTTP_HOST, HTTP_KEY, HTTP_USER_AGENT"
            }}
        )

        # With variables
        self.assertEqual(
            client.execute("query MyQuery($myVar: String) { name(suffix: $myVar) }", variables={"myVar": "..."}),
            {"data": {"name": "The Republic of Heaven..."}}
        )

        # History
        self.assertEqual(client.history[0][0], {
            "query": "query MyQuery($myVar: String) { name(suffix: $myVar) }",
            "variables": {"myVar": "..."}
        })
        self.assertEqual(client.history[0][1], {"data": {"name": "The Republic of Heaven..."}})
        self.assertEqual(client.history[1][0], {"query": "{ name headers}", "variables": {}})
        self.assertEqual(client.history[1][1], {"data": {
            "name": "The Republic of Heaven",
            "headers": "HTTP_ACCEPT, HTTP_ACCEPT_ENCODING, HTTP_CONNECTION, HTTP_COOKIE, HTTP_HOST, HTTP_KEY, HTTP_USER_AGENT"
        }})


    def test_quick_function(self):
        # Basic
        self.assertEqual(
            kirjava.execute(self.live_server_url, "{ name }"),
            {"data": {"name": "The Republic of Heaven"}}
        )

        # With headers
        self.assertEqual(
            kirjava.execute(self.live_server_url, "{ name headers}", headers={"KEY": "VALUE"}),
            {"data": {
                "name": "The Republic of Heaven",
                "headers": "HTTP_ACCEPT, HTTP_ACCEPT_ENCODING, HTTP_CONNECTION, HTTP_HOST, HTTP_KEY, HTTP_USER_AGENT"
            }}
        )

        # With variables
        self.assertEqual(
            kirjava.execute(
                self.live_server_url, "query MyQuery($myVar: String) { name(suffix: $myVar) }",
                variables={"myVar": "..."}
            ),
            {"data": {"name": "The Republic of Heaven..."}}
        )
    

    def test_image_upload(self):
        client = kirjava.Client(self.live_server_url)
        with open(os.devnull, "w") as fnull:
            with redirect_stderr(fnull) as err:
                with open("kirjava/client.py") as f:
                    result = client.execute("""mutation uploadImage($image: Upload!) {
                        uploadImage(image: $image) { information }
                    }""", variables={"image": f})            
        self.assertEqual(
            result["data"]["uploadImage"]["information"],
            "{'image': <InMemoryUploadedFile: client.py (text/x-python)>}"
        )
    

    def test_multi_image_upload(self):
        client = kirjava.Client(self.live_server_url)
        with open("kirjava/client.py") as f1:
            with open("kirjava/utilities.py") as f2:
                result = client.execute("""mutation uploadImages($images: [Upload]!) {
                    uploadImages(images: $images) { information }
                }""", variables={"images": [f1, f2]})
        self.assertEqual(
            result["data"]["uploadImages"]["information"],
            "{'images': [<InMemoryUploadedFile: client.py (text/x-python)>, <InMemoryUploadedFile: utilities.py (text/x-python)>]}"
        )

