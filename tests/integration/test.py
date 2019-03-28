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

    def test(self):
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