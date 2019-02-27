import unittest

from ..utils.crypt import encrypt, decrypt

class TestCryptMethod(unittest.TestCase):

    def testEncrypt(self):
        self.assertEqual(encrypt("a"), "c")
        self.assertEqual(encrypt("z"), "1")
        self.assertEqual(encrypt("9"), "b")


    def testDecrypt(self):
        self.assertEqual(decrypt("c"), "a")
        self.assertEqual(decrypt("1"), "z")
        self.assertEqual(decrypt("b"), "9")


if __name__ == "__main__":
    unittest.main()