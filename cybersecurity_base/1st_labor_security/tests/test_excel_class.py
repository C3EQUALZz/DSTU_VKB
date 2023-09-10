from unittest import TestCase, main

import aspose.cells as ac

from ..realisation_classes.excel_class import ExcelBlock
from ..realisation_classes.word_class import BadPassword


class ExcelTest(TestCase):
    correct_path: str = ('/home/c3equalz/Рабочий стол/Основы информационной безопасности/Лабораторная '
                         '1/files_for_test/ЭВМ_Ковалев_ВКБ12.xlsx')
    correct_excel_file = ExcelBlock(correct_path)

    workbook_for_test = ac.Workbook(correct_path)

    def test_path(self):
        self.assertEqual(ExcelTest.correct_excel_file.path, ExcelTest.correct_path)

    def test_path_setter(self):
        path = '/home/c3equalz/Загрузки/Криптография_с_секретным_ключом_2023_Фрэнк_Рубин_.pdf'
        with self.assertRaises(ValueError) as error:
            ExcelBlock(path)
        self.assertEqual("Неправильный путь к файлу, проверьте снова ", error.exception.args[0])

    def test_key_getter_default(self):
        self.assertEqual("FULL", ExcelTest.correct_excel_file.key)

    def test_key_getter_other(self):
        another_word_file = ExcelBlock(ExcelTest.correct_path)
        another_word_file.key = 'contents'
        self.assertEqual("CONTENTS", another_word_file.key)

    def test_key_error(self):
        another_word_file = ExcelBlock(ExcelTest.correct_path)
        with self.assertRaises(KeyError) as error:
            another_word_file.key = "abracadabra"
        self.assertEqual("Не подходящий ключ для указания значения ", error.exception.args[0])

    def test_block_file(self):
        ExcelTest.correct_excel_file.unblock_file("123456")

        ExcelTest.correct_excel_file.block_file("123456")
        info = ac.FileFormatUtil.detect_file_format(self.correct_path)
        self.assertTrue(info.is_encrypted)

        ExcelTest.correct_excel_file.unblock_file("123456")
        new_info = ac.FileFormatUtil.detect_file_format(self.correct_path)
        self.assertFalse(new_info.is_encrypted)

    def test_default_unblock_file(self):
        info = ac.FileFormatUtil.detect_file_format(self.correct_path)
        self.assertFalse(info.is_encrypted)

    def test_check_correct_password_length(self):
        with self.assertRaises(BadPassword) as error:
            ExcelTest.correct_excel_file.block_file("123")
        self.assertEqual("В вашем пароле должно быть больше 5 символов, обязательно наличие хотя бы одной цифры ",
                         error.exception.args[0])
        self.test_default_unblock_file()

    def test_check_correct_type_password(self):
        with self.assertRaises(BadPassword) as error:
            ExcelTest.correct_excel_file.block_file(123)
        self.assertEqual("В вашем пароле должно быть больше 5 символов, обязательно наличие хотя бы одной цифры ",
                         error.exception.args[0])
        self.test_default_unblock_file()

    def test_unblock_list(self):
        try:
            ExcelTest.correct_excel_file.unblock_list(0, "123456")
        except RuntimeError:
            ...
        sheet = ExcelTest.workbook_for_test.worksheets.get(0)
        self.assertFalse(sheet.protection.is_protected_with_password)

    def test_block_list(self):
        ExcelTest.correct_excel_file.block_list(0, "123456")

        workbook = ac.Workbook(ExcelTest.correct_path)
        sheet = workbook.worksheets.get(0)
        self.assertTrue(sheet.protection.is_protected_with_password)

        ExcelTest.correct_excel_file.unblock_list(0, "123456")
        workbook = ac.Workbook(ExcelTest.correct_path)
        sheet = workbook.worksheets.get(0)
        self.assertFalse(sheet.protection.is_protected_with_password)

    def test_block_ranges(self):
        ExcelTest.correct_excel_file.block_range(0, "A1:C3")
        workbook = ac.Workbook(ExcelTest.correct_path)
        sheet = workbook.worksheets.get(0)

        for letter_number in range(0, 3):
            for number in range(1, 4):
                cell = chr(65 + letter_number) + str(number)
                style = sheet.cells.get(cell).get_style()
                self.assertTrue(style.is_locked)

        self.assertFalse(
            all(x.is_locked for x in (sheet.cells.get("A4").get_style(), sheet.cells.get("A25").get_style(),
                                      sheet.cells.get("A5").get_style(), sheet.cells.get("B4").get_style()))
        )

    def test_unblock_ranges(self):
        ExcelTest.correct_excel_file.unblock_range(0, "A1:C3")
        workbook = ac.Workbook(ExcelTest.correct_path)
        sheet = workbook.worksheets.get(0)

        for letter_number in range(0, 3):
            for number in range(1, 4):
                cell = chr(65 + letter_number) + str(number)
                style = sheet.cells.get(cell).get_style()
                self.assertFalse(style.is_locked)


if __name__ == '__main__':
    main()
