import random
import unittest
import actandra

class TestActandra(unittest.TestCase):

    def setUp(self):
        actandra._truncate()

    def test_subscribe(self):
        self.assertEquals([], actandra.get_subscribers('elvis'))
        actandra.subscribe('elvis', 'frank')
        actandra.subscribe('elvis', 'julia')
        self.assertEquals(['frank', 'julia'], actandra.get_subscribers('elvis'))

    def test_unsubscribe(self):
        actandra.subscribe('elvis', 'frank')
        actandra.subscribe('elvis', 'julia')
        actandra.unsubscribe('elvis', 'frank')
        self.assertEquals(['julia'], actandra.get_subscribers('elvis'))

    def test_get_subscribers(self):
        # Tested through subscribe/unsubscribe
        pass

if __name__ == '__main__':
    unittest.main()

