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
        client = kirjava.Client(self.live_server_url)
        self.assertEqual(
         client.execute("{ name }"),
         {"data": {"name": "The Republic of Heaven"}}
        )
