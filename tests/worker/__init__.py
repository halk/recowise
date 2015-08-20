import os
import unittest
from core.config import Config

class WorkerTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Config(os.path.join(
            os.path.dirname(__file__), '..', 'config', 'config.xml'
        ))
