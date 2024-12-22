from unittest import TestCase, main

import aspose.words as aw

from ..realisation_classes.word_class import WordBlock, BadPassword


class WordTest(TestCase):
    correct_path: str = ('/home/c3equalz/Рабочий стол/Основы информационной безопасности/Лабораторная '
                         '1/files_for_test/ЭВМ_Ковалев_ВКБ12.docx')
    correct_word_file = WordBlock(correct_path)

    def test_path(self):
        self.assertEqual(WordTest.correct_word_file.path, WordTest.correct_path)

    def test_path_setter(self):
        path = '/home/c3equalz/Загрузки/Криптография_с_секретным_ключом_2023_Фрэнк_Рубин_.pdf'
        with self.assertRaises(ValueError) as error:
            WordBlock(path)
        self.assertEqual("Неправильный путь к файлу, проверьте снова ", error.exception.args[0])

    def test_key_getter_default(self):
        self.assertEqual("FULL", WordTest.correct_word_file.key)

    def test_key_getter_other(self):
        another_word_file = WordBlock(WordTest.correct_path)
        another_word_file.key = "read_only"
        self.assertEqual("READ_ONLY", another_word_file.key)

    def test_key_error(self):
        another_word_file = WordBlock(WordTest.correct_path)
        with self.assertRaises(KeyError) as error:
            another_word_file.key = "abracadabra"
        self.assertEqual("Не подходящий ключ для указания значения ", error.exception.args[0])

    def test_block_file(self):
        WordTest.correct_word_file.block_file("123456")
        info = aw.FileFormatUtil.detect_file_format(self.correct_path)
        self.assertTrue(info.is_encrypted)

        WordTest.correct_word_file.unblock_file("123456")
        new_info = aw.FileFormatUtil.detect_file_format(self.correct_path)
        self.assertFalse(new_info.is_encrypted)

    def test_default_unblock_file(self):
        info = aw.FileFormatUtil.detect_file_format(self.correct_path)
        self.assertFalse(info.is_encrypted)

    def test_check_correct_password_length(self):
        with self.assertRaises(BadPassword) as error:
            WordTest.correct_word_file.block_file("123")
        self.assertEqual("В вашем пароле должно быть больше 5 символов, обязательно наличие хотя бы одной цифры ",
                         error.exception.args[0])
        self.test_default_unblock_file()

    def test_check_correct_type_password(self):
        with self.assertRaises(BadPassword) as error:
            WordTest.correct_word_file.block_file(123)
        self.assertEqual("В вашем пароле должно быть больше 5 символов, обязательно наличие хотя бы одной цифры ",
                         error.exception.args[0])
        self.test_default_unblock_file()


if __name__ == "__main__":
    main()
