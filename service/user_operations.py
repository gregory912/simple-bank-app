from .validation import *
from .user_actions import *
from .security.security import Security
from service.history_service import SearchTransactions
from service.transactions_service import SaveTransactions
import random
from decimal import Decimal
from typing import Callable


class UserOperations:
    def __init__(self):
        self._sequence = 0
        self._logged_in_user = dict()
        self._chosen_account = 0
        self._available_accounts = dict()
        self._val_obj = Validation()
        self._qry_obj = UserActions()
        self._sec_obj = Security()
        self._sear_eng = SearchTransactions()
        self._save_transactions = SaveTransactions()

    def _does_account_exist(self):
        """The function checks if the user wants to create an account.
        The _sequence variable is given the appropriate value"""
        print(f"{' ' * 12}Do you have a bank account?")
        response = self.get_answer(
            self._val_obj.validation_of_answer,
            "Enter Y or N: ",
            'Entered value is not correct. Enter Y or N: ')
        self._sequence = 10 if response == 'Y' else 1

    def _create_account(self):
        """Create an account for the new user.
        Check if the user with the given data does not exist anymore. Enter full user details."""
        print(f'{" " * 12}Would you like to create an account?')
        response = self.get_answer(
            self._val_obj.validation_of_answer,
            "Enter Y or N: ",
            'Entered value is not correct. Enter Y or N: ')
        if response == 'Y':
            while True:
                login = self.get_answer(
                    self._val_obj.validation_alnum_and_not_digit,
                    'Enter Login: ',
                    'Entered data contains illegal characters. Try again: ')
                password = self._sec_obj.encode(self.get_answer(
                    self._val_obj.validation_alnum_and_not_digit,
                    'Enter Password: ',
                    'Entered data contains illegal characters. Try again: '))
                if self._qry_obj.check_user(login):
                    print(f'{" " * 12}Entered login is already used. Enter another login.')
                else:
                    break
            print('Enter user data:')
            name = self.get_answer(
                self._val_obj.validation_alpha,
                'Enter your name: ',
                'Entered data contains illegal characters. Try again: ')
            surname = self.get_answer(
                self._val_obj.validation_alpha,
                'Enter your surname: ',
                'Entered data contains illegal characters. Try again: ')
            address = self.get_answer(
                self._val_obj.validation_space_or_alpha_not_digit,
                'Enter your address: ',
                'Entered data contains illegal characters. Try again: ')
            email = self.get_answer(
                self._val_obj.validation_email,
                'Enter your email: ',
                'Entered data contains illegal characters. Try again: ')
            phone = self.get_answer(
                self._val_obj.validation_digit,
                'Enter your phone: ',
                'Entered number should contain between 9 and 11 characters. Try again: ',
                (9, 11))
            pesel = self.get_answer(
                self._val_obj.validation_digit,
                'Enter your Personal ID Number: ',
                'Entered number should contain between 10 and 11 characters. Try again: ',
                (10, 11))
            lastrow = self._qry_obj.insert_user(login, password)
            self._qry_obj.insert_customer(lastrow, name, surname, address, email, phone, pesel)
            print(f'{" " * 12}Your account has been created')
            self._sequence = 10
        else:
            raise SystemExit(0)

    def _login(self):
        """Login the user. The entered password is encoded and compared with the password in the database"""
        while True:
            login = input('Enter your login: ')
            password = input('Enter your password: ')
            try:
                self._logged_in_user = self._qry_obj.find_user(login, password).__dict__
                print(f'\n{" " * 12}Welcome in your bank account.')
                break
            except AttributeError:
                print(f'{" " * 12}Account not found for the given data. Try again.')
        self._sequence = 15

    def _show_accounts(self):
        """Show all available user accounts"""
        accounts = self._qry_obj.get_all_accounts(self._logged_in_user['login'])
        if accounts:
            print("""
            Available accounts:""")
            self._available_accounts = {x: accounts[x - 1] for x in range(1, len(accounts) + 1)}
            for key, value in self._available_accounts.items():
                print(f'{" " * 12}{key} - Account name: {value[4]}. Account number: {value[5]}. '
                      f'Balance {0 if not value[6] else value[6]}. '
                      f'Bussines account: {"YES" if value[8] else "NO"}')
        else:
            print("""
            You do not currently have any account available. Would you like to open an account?
            """)
            response = self.get_answer(
                self._val_obj.validation_of_answer,
                "Enter Y or N: ",
                'Entered value is not correct. Enter Y or N: ')
            if response == 'Y':
                self._create_bank_account()

    def _create_bank_account(self):
        """Get data from user. Generate a bank account number and create a new account. ,
        Ask the user if they want an individual or business account that requires more information."""
        print(f'{" " * 12}Would you like to create a bussines account?')
        response = self.get_answer(
            self._val_obj.validation_of_answer,
            "Enter Y or N: ",
            'Entered value is not correct. Enter Y or N: ')
        entered_acc_name = self.get_answer(
            self._val_obj.validation_space_or_alpha_not_digit,
            'Enter a bank account name: ',
            'Entered data contains illegal characters. Try again: ')
        while True:
            bank_acc_number = self.get_ran_num(0, 9, 26)
            if not self._qry_obj.check_bank_account(bank_acc_number):
                break
        if response == 'Y':
            lastrow_ba = self._qry_obj.insert_bank_account(
                entered_acc_name,
                bank_acc_number,
                commision=int(self.get_ran_num(1, 10, 1))
            )
            print(f'{" " * 12}Enter company details: ')
            company_name = self.get_answer(
                self._val_obj.validation_space_or_alpha_not_digit,
                'Enter company name: ',
                'Entered data contains illegal characters. Try again: ')
            company_address = self.get_answer(
                self._val_obj.validation_space_or_alpha_not_digit,
                'Enter company address: ',
                'Entered data contains illegal characters. Try again: ')
            while True:
                nip = self.get_answer(
                    self._val_obj.validation_digit,
                    'Enter NIP number: ',
                    'Entered number should contain between 7 and 9 characters. Try again: ',
                    (7, 9))
                if not self._qry_obj.check_nip(nip):
                    break
                else:
                    print(f'{" " * 12}A company account with the given NIP number already exists. Please try again')
            regon = self.get_answer(
                self._val_obj.validation_digit,
                'Enter REGON number: ',
                'Entered number should contain between 7 and 9 characters. Try again: ',
                (7, 9))
            lastrow_cd = self._qry_obj.insert_company_detail(company_name, company_address, nip, regon)
            self._qry_obj.insert_profile(self._qry_obj.get_customer_id(
                self._logged_in_user['id']).id, lastrow_ba, lastrow_cd)
        else:
            lastrow_ba = self._qry_obj.insert_bank_account(entered_acc_name, bank_acc_number)
            self._qry_obj.insert_profile(self._qry_obj.get_customer_id(self._logged_in_user['id']).id, lastrow_ba)
        print(f'\n{" " * 12}Bank account has been created successfully.')

    def _add_money(self, chosen_account: int):
        """Enter the transfer details and add the money to the selected account."""
        data = self._available_accounts[chosen_account]
        transfer_amount = Decimal(self.get_answer(
            self._val_obj.validation_decimal,
            'Enter transfer amount: ',
            'Entered data contains illegal characters. Try again: '))
        payer_name = self.get_answer(
            self._val_obj.validation_space_or_alpha_not_digit,
            'Enter the name of the payer: ',
            'Entered data contains illegal characters. Try again: ')
        trans_name = self.get_answer(
            self._val_obj.validation_space_or_alpha_not_digit,
            'Enter transaction name: ',
            'Entered data contains illegal characters. Try again: ')
        if len(self._qry_obj.get_transactions_betwn_dates(date.today(), data[9])) > 5 and data[7]:
            new_amount = data[6] + (transfer_amount - (transfer_amount * Decimal(data[8]/100)))
            print(f'\n{" " * 12}You have made more than 5 money transfers this month')
            print(f'{" " * 12}The commission {data[8]}% has been taken from your transfers.')
        else:
            new_amount = data[6] + transfer_amount
        self._qry_obj.update_bank_account(data[9], data[4], data[5], new_amount, data[8])
        self._qry_obj.insert_transaction(data[3], 'YES', None, transfer_amount, data[5], payer_name, trans_name)

    def _transfer_money(self, chosen_account: int):
        """Enter your transfer details and send the money"""
        data = self._available_accounts[chosen_account]
        transfer_amount = Decimal(self.get_answer(
            self._val_obj.validation_decimal,
            'Enter the amount you want to transfer: ',
            'Entered data contains illegal characters. Try again: '))
        if data[7]:
            new_amount = data[6] - (transfer_amount + (transfer_amount * Decimal(data[8] / 100)))
        else:
            new_amount = data[6] - transfer_amount
        if new_amount < 0:
            print(f'\n{" " * 12}You do not have sufficient funds to make the transfer.')
        else:
            rcpt_name = self.get_answer(
                self._val_obj.validation_space_or_alpha_not_digit,
                'Enter recipent name: ',
                'Entered data contains illegal characters. Try again: ')
            trans_name = self.get_answer(
                self._val_obj.validation_space_or_alpha_not_digit,
                'Enter transaction name: ',
                'Entered data contains illegal characters. Try again: ')
            acc_num = self.get_answer(
                self._val_obj.validation_digit,
                'Enter the account number to which you want to transfer money: ',
                'Entered number should contain between 24 and 26 characters. Try again: ',
                (24, 26))
            if data[7]:
                print(f'\n{" " * 12}The regular commission for the business account'
                      f' {data[8]}% has been taken from your transfers.')
            self._qry_obj.update_bank_account(data[9], data[4], data[5], new_amount, data[8])
            self._qry_obj.insert_transaction(data[3], None, 'YES', transfer_amount, acc_num, rcpt_name, trans_name)

    def _history(self):
        """Check the history of your transactions. Choose from options to search the story or show the full story."""
        print("""
            Select operation for your history:
            1. Search your payment history
            2. Show the full history
        """)
        chosen_operation = self.get_answer(
            self._val_obj.validation_chosen_operation,
            'Enter chosen operation: ',
            'Entered data contains illegal characters. Try again: ',
            (1, 2))
        match chosen_operation:
            case '1':
                entered_value = input('Enter the item to search for: ')
                transactions = self._sear_eng.search_elements(self._qry_obj.get_trans_for_user(
                    self._logged_in_user['login']), entered_value)
                if transactions:
                    print(f'\n{" " * 12}Search Results:')
                    self._sear_eng.print_data(transactions)
                    self._save_data(transactions)
                else:
                    print(f'\n{" " * 12}No results found for your search')
            case '2':
                transactions = self.get_list_of_dict(self._qry_obj.get_trans_for_user(self._logged_in_user['login']))
                if transactions:
                    print(f'\n{" " * 12}Search Results:')
                    self._sear_eng.print_data(transactions)
                    self._save_data(transactions)
                else:
                    print(f'\n{" " * 12}No results found for your search')

    def _save_data(self, transactions: list[dict]):
        """Save data to JSON, CSV or PDF formats. Enter the path where the file should be saved"""
        print(f'\n{" " * 12}Would you like to save the history?')
        response = self.get_answer(
            self._val_obj.validation_of_answer,
            "Enter Y or N: ",
            'Entered value is not correct. Enter Y or N: ')
        if response == 'Y':
            print("""
                Select the format in which you would like to save the data:
                1. JSON
                2. CSV
                3. PDF
            """)
            chosen_operation = self.get_answer(
                self._val_obj.validation_chosen_operation,
                'Enter chosen operation: ',
                'Entered data contains illegal characters. Try again: ',
                (1, 3))
            file_path = self.get_answer(
                self._val_obj.validation_file_path,
                r"Enter the path to the file in the format  C:\Folder\Subfolder  : ",
                'The path entered does not exist. Try again')
            file_name = self.get_answer(
                self._val_obj.validation_file_name,
                r"Enter a file name without an extension: ",
                'Entered data contains illegal characters. Try again')
            match chosen_operation:
                case '1':
                    self._save_transactions.serialize(transactions, 'json', file_path,
                                                      file_name, self._logged_in_user['login'])
                case '2':
                    self._save_transactions.serialize(transactions, 'csv', file_path,
                                                      file_name, self._logged_in_user['login'])
                case '3':
                    self._save_transactions.serialize(transactions, 'pdf', file_path,
                                                      file_name, self._logged_in_user['login'])

    def _choose_operation(self):
        """The main menu of the program where you can select the operation to be performed"""
        print("""
            Select operation for your account: 
            1. Open a bank account
            2. Add money
            3. Make a transfer
            4. Check history of transactions
            5. Show available accounts
            6. Log out
            """)
        chosen_operation = self.get_answer(
            self._val_obj.validation_chosen_operation,
            'Enter chosen operation: ',
            'Entered data contains illegal characters. Try again: ',
            (1, 6))
        match chosen_operation:
            case '1':
                self._create_bank_account()
            case '2':
                if self._available_accounts:
                    self._show_accounts()
                    chosen_account = int(self.get_answer(
                        self._val_obj.validation_choose_account,
                        '\nSelect the account number: ',
                        'You selected the wrong account. Try again: ',
                        (self._available_accounts,)))
                    self._add_money(chosen_account)
                else:
                    self._show_accounts()
            case '3':
                if self._available_accounts:
                    self._show_accounts()
                    chosen_account = int(self.get_answer(
                        self._val_obj.validation_choose_account,
                        '\nSelect the account number: ',
                        'You selected the wrong account. Try again: ',
                        (self._available_accounts,)))
                    self._transfer_money(chosen_account)
                else:
                    self._show_accounts()
            case '4':
                self._history()
            case '5':
                self._show_accounts()
            case '6':
                raise SystemExit(0)

    def call_cycle(self):
        """A cycle that controls the program accordingly"""
        match self._sequence:
            case 0:
                self._does_account_exist()
            case 1:
                self._create_account()
            case 10:
                self._login()
            case 15:
                self._choose_operation()

    @staticmethod
    def get_ran_num(min_range: int, max_range: int, amount: int) -> str:
        """Generate random number"""
        return ''.join([str(random.randint(min_range, max_range)) for _ in range(amount)])

    @staticmethod
    def get_list_of_dict(items: iter) -> list[dict]:
        """Generate a dictionary of component fields from the indicated list of objects"""
        return [item.__dict__ for item in items]

    @staticmethod
    def get_answer(function: Callable, description: str, wrong_answer: str, args: tuple = None) -> str:
        """Check the validation of the entered element on the basis of the entered validation function"""
        def get_tuple():
            return (entered_answer,) if not args else tuple([x for x in [entered_answer] + [x for x in args]])
        while True:
            entered_answer = input(description)
            if function(*get_tuple()):
                return entered_answer
            else:
                print(wrong_answer)
