import unittest
from engines.in_common import Engine
from tests.engines import BaseEngineTestCase

class EngineTestCase(BaseEngineTestCase, unittest.TestCase):
    def setUp(self):
        self._setUp(Engine, 'in_common')
