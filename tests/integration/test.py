

import sys
import os
#sys.path.append(os.path.join("..", "zincbind"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.integration.testserver.settings")
import django; django.setup()

from django.contrib.staticfiles.testing import LiveServerTestCase

class Test(LiveServerTestCase):

    def test(self):
        pass
