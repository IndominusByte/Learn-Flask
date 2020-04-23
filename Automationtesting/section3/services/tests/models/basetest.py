import os,sys
from unittest import TestCase

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../../')
sys.path.append(basedir)

class BaseTest(TestCase):
    def setUp(self):
        pass
