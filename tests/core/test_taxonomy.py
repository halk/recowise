import unittest
from core.taxonomy import Taxonomy

class TaxonomyTestCase(unittest.TestCase):
    def setUp(self):
        self.taxonomy = Taxonomy('test', {
            'key': 'value',
            'key2': 'value2',
            'key3': 'value3',
        })

    def test_get_name(self):
        self.assertEqual(self.taxonomy.get_name(), 'test')

    def test_get_taxons(self):
        taxons = self.taxonomy.get_taxons()
        self.assertEqual(taxons, {
            'key': 'value',
            'key2': 'value2',
            'key3': 'value3',
        })
        self.assertEqual(len(taxons), 3)

    def test_get(self):
        self.assertEqual(self.taxonomy.get('key'), 'value')
        self.assertEqual(self.taxonomy.get('key2'), 'value2')
        self.assertIsNone(self.taxonomy.get('key4'))

    def test_inherit(self):
        parentTaxonomy = Taxonomy('parentTest', {'key5': 'value5'})
        self.assertEqual(parentTaxonomy.get('key5'), 'value5')
        self.assertIsNone(self.taxonomy.get('key4'))
        self.assertIsNone(parentTaxonomy.get('key4'))

        parentParentTaxonomy = Taxonomy('parentTest', {'key4': 'value4'})
        parentTaxonomy.inherit(parentParentTaxonomy)
        self.assertEqual(parentTaxonomy.get('key4'), 'value4')

        self.taxonomy.inherit(parentTaxonomy)
        self.assertEqual(self.taxonomy.get('key4'), 'value4')
        self.assertEqual(self.taxonomy.get('key5'), 'value5')

    def test_translate(self):
        translated = self.taxonomy.translate({'value': 'asd', 'value3': 'qwe'})
        self.assertEqual(translated, {'key': 'asd', 'key2': 'value2', 'key3': 'qwe'})
