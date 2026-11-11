import unittest
from src.monitor import classify, safe_url, check_product

class ScannerTests(unittest.TestCase):
    def test_sold_out(self): self.assertEqual(classify('<div>Ausverkauft</div>'), 'unavailable')
    def test_positive(self): self.assertEqual(classify('<button>Add to cart</button>'), 'possible_stock')
    def test_conflict(self): self.assertEqual(classify('<p>Out of stock</p><button>Add to cart</button>'), 'uncertain')
    def test_ambiguous(self): self.assertEqual(classify('<p>Product information</p>'), 'unknown')
    def test_url_safety(self):
        for url in ['http://example.com','http://localhost','https://127.0.0.1','file:///etc/passwd','https://user:pass@localhost']:
            self.assertFalse(safe_url(url))
        self.assertTrue(safe_url('https://example.org/item'))
    def test_no_url_leak(self): self.assertEqual(check_product({'name': 'test','url': 'file:///secret'})['url'], '')

if __name__ == '__main__': unittest.main()
