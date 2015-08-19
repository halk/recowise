import os
import unittest
import lxml
from lxml import etree

class ConfigXsdTestCase(unittest.TestCase):
    def validate_schema(self, file):
        curdir = os.path.dirname(os.path.realpath(__file__))
        with open(curdir + '/../../config/config.xsd') as f:
            doc = etree.parse(f)
        schema = etree.XMLSchema(doc)

        with open(curdir + file) as f:
            doc = etree.parse(f)

        schema.assertValid(doc)

    def test_reference_config_validity(self):
        self.validate_schema('/config.xml')

    def test_active_config_validity(self):
        self.validate_schema('/../../config/config.xml')
