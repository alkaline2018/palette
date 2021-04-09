import unittest
from datetime import datetime

from util import create_directory


class MyTestCase(unittest.TestCase):
    def test_create_directory(self):
        now_date = datetime.now()
        now_dir_structure = now_date.strftime("%Y/%m/%d/%H/%M")
        create_directory("../public/image/"+now_dir_structure)
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
