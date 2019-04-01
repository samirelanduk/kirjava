import sys
import os
os.environ.setdefault(
 "DJANGO_SETTINGS_MODULE", "tests.integration.testserver.settings"
)
import django; django.setup()
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.test.utils import override_settings
import kirjava

@override_settings(DEBUG=True)
class Test(LiveServerTestCase):

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
          "headers": "HTTP_ACCEPT, HTTP_ACCEPT_ENCODING, HTTP_CONNECTION, HTTP_HOST, HTTP_KEY, HTTP_USER_AGENT"
         }}
        )

        # With variables
        self.assertEqual(
         client.execute("query MyQuery($myVar: String) { name(suffix: $myVar) }", variables={"myVar": "..."}),
         {"data": {"name": "The Republic of Heaven..."}}
        )

        # History
        self.assertEqual(client.history[0][0], {
         "string": "query MyQuery($myVar: String) { name(suffix: $myVar) }",
         "variables": {"myVar": "..."}
        })
        self.assertEqual(client.history[0][1], {"data": {"name": "The Republic of Heaven..."}})
        self.assertEqual(client.history[1][0], {"string": "{ name headers}", "variables": {}})
        self.assertEqual(client.history[1][1], {"data": {
         "name": "The Republic of Heaven",
         "headers": "HTTP_ACCEPT, HTTP_ACCEPT_ENCODING, HTTP_CONNECTION, HTTP_HOST, HTTP_KEY, HTTP_USER_AGENT"
        }})


    def test_quick_function(self):
        self.assertEqual(
         kirjava.execute(self.live_server_url, "{ name }"),
         {"data": {"name": "The Republic of Heaven"}}
        )
