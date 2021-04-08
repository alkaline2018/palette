import unittest
import uuid


class MyTestCase(unittest.TestCase):
    def test_uuid(self):
        url = 'https://dpdpwl.tistory.com/'
        print(uuid.uuid3(uuid.NAMESPACE_URL, url))
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
