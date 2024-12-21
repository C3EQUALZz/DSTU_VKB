import os
from unittest import TestCase
########################################################################################################################
from PIL import Image
########################################################################################################################
from ..backend_сipher import Cypher


class TestCipher(TestCase):

    def test_crypt(self):
        image = Image.open("third_laba/test/baz.jpg")
        cypher = Cypher(image)
        encrypted_image = cypher.encrypt(key_filename="third_laba/test/key_test.txt")
        encrypted_image.save("third_laba/test/baz_encrypted.png")
        self.assertTrue(os.path.exists("third_laba/test/baz_encrypted.png"))

    def test_decrypt(self):
        image = Image.open("third_laba/test/baz_encrypted.png")
        cypher = Cypher(image)
        decrypted_image = cypher.decrypt(key_filename="third_laba/test/key_test.txt")
        decrypted_image.save("third_laba/test/baz_decrypted.png")
        self.assertTrue(os.path.exists("third_laba/test/baz_decrypted.png"))
