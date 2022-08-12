import unittest
from service.validation import Validation


class TestCrudRepo(unittest.TestCase):
    def setUp(self):
        self._val_obj = Validation()

    def test_validation_of_answer(self):
        """Test if method returns True only for Y and N"""
        self.assertTrue(self._val_obj.validation_of_answer('Y'))
        self.assertTrue(self._val_obj.validation_of_answer('N'))
        self.assertFalse(self._val_obj.validation_of_answer('a'), False)
        self.assertFalse(self._val_obj.validation_of_answer('1'), False)

    def test_alnum_and_not_digit(self):
        """Test if method returns True for letters and numbers"""
        self.assertTrue(self._val_obj.validation_alnum_and_not_digit('abc123'))
        self.assertTrue(self._val_obj.validation_alnum_and_not_digit('ABC123'))
        self.assertFalse(self._val_obj.validation_alnum_and_not_digit('a b'), False)
        self.assertFalse(self._val_obj.validation_alnum_and_not_digit('1'), False)

    def test_alpha(self):
        """Test if method returns True for letters"""
        self.assertTrue(self._val_obj.validation_alpha('abc'))
        self.assertTrue(self._val_obj.validation_alpha('ABC'))
        self.assertFalse(self._val_obj.validation_alpha('a b'), False)
        self.assertFalse(self._val_obj.validation_alpha('1 '), False)

    def test_digit(self):
        """Test if method returns True for digits"""
        self.assertTrue(self._val_obj.validation_digit('123', 2, 3))
        self.assertTrue(self._val_obj.validation_digit('987', 2, 3))
        self.assertFalse(self._val_obj.validation_digit('a b', 2, 3), False)
        self.assertFalse(self._val_obj.validation_digit('a 1', 2, 3), False)

    def test_space_or_alpha_not_digit(self):
        """Test if method returns True for letters, spaces and digits"""
        self.assertTrue(self._val_obj.validation_space_or_alpha_not_digit('abc 123'))
        self.assertTrue(self._val_obj.validation_space_or_alpha_not_digit('a8'))
        self.assertFalse(self._val_obj.validation_space_or_alpha_not_digit('123'), False)
        self.assertFalse(self._val_obj.validation_space_or_alpha_not_digit('1 2'), False)
        self.assertFalse(self._val_obj.validation_space_or_alpha_not_digit('12 '), False)
        self.assertFalse(self._val_obj.validation_space_or_alpha_not_digit(' 12'), False)

    def test_decimal(self):
        """Test if method returns True for string which will be converted to Decimal"""
        self.assertTrue(self._val_obj.validation_decimal('12.52'))
        self.assertTrue(self._val_obj.validation_decimal('100'))
        self.assertFalse(self._val_obj.validation_decimal('11,11'), False)
        self.assertFalse(self._val_obj.validation_decimal('14 1'), False)

    def test_email(self):
        """Test if method returns True for string which an email"""
        self.assertTrue(self._val_obj.validation_email('user@email.com'))
        self.assertTrue(self._val_obj.validation_email('user.name@email.com'))
        self.assertFalse(self._val_obj.validation_email('usernameemail.com'), False)
        self.assertFalse(self._val_obj.validation_email('username&email.com'), False)

    def test_chosen_operation(self):
        """Test if method returns True for chosen digit of operation"""
        self.assertTrue(self._val_obj.validation_chosen_operation('1', 1, 3))
        self.assertTrue(self._val_obj.validation_chosen_operation('2', 1, 3))
        self.assertFalse(self._val_obj.validation_chosen_operation('4', 1, 3), False)
        self.assertFalse(self._val_obj.validation_chosen_operation('a', 1, 3), False)

    def test_choose_account(self):
        """Test if method returns True for chosen digit of account"""
        self.assertTrue(self._val_obj.validation_choose_account('1', {1: 'one', 2: 'two'}))
        self.assertTrue(self._val_obj.validation_choose_account('1', {1: 'one', 2: 'two'}))
        self.assertFalse(self._val_obj.validation_choose_account('3', {1: 'one', 2: 'two'}), False)
        self.assertFalse(self._val_obj.validation_choose_account('one', {1: 'one', 2: 'two'}), False)

    def test_file_name(self):
        """Test if method returns True for file name which include only permitted characters"""
        self.assertTrue(self._val_obj.validation_file_name('file'))
        self.assertTrue(self._val_obj.validation_file_name('file_123'))
        self.assertFalse(self._val_obj.validation_file_name('file/'), False)
        self.assertFalse(self._val_obj.validation_file_name('file*'), False)

    def test_file_path(self):
        """Test if method returns True for file path which exists"""
        self.assertTrue(self._val_obj.validation_file_path('C:\\'))
        self.assertFalse(self._val_obj.validation_file_path('C:\\*'), False)
        self.assertFalse(self._val_obj.validation_file_path('C:\\?'), False)


if __name__ == '__main__':
    unittest.main()
