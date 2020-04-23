import os,sys
from unittest import TestCase
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../../')
sys.path.append(basedir)

from app import app

class BaseTest(TestCase):
    def setUp(self):
        self.app = app.test_client
