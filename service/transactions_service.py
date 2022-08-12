from service.save_data.save_json import OperationsJSON
from service.save_data.save_csv import OperationsCSV
from service.save_data.save_pdf import OperationsPDF
from typing import Callable


class SaveTransactions:
    def __init__(self):
        self._json_obj = OperationsJSON()
        self._csv_obj = OperationsCSV()
        self._pdf_obj = OperationsPDF('P', 'mm', 'A4')

    def serialize(self, transactions: list[dict], format_: str, file_path: str, file_name: str, user: str):
        """Writing to a file based on the received format"""
        serializer = self.get_serializer(format_)
        path = self.create_path(file_path, file_name, format_)
        transactions = self.unpack_data(transactions)
        serializer(transactions, path, user)

    def get_serializer(self, format_: str) -> Callable:
        """Return function for the required format"""
        if format_ == 'json':
            return self._serialize_to_json
        elif format_ == 'csv':
            return self._serialize_to_csv
        elif format_ == 'pdf':
            return self._serialize_to_pdf
        else:
            raise ValueError(format_)

    def _serialize_to_json(self, transactions: list, path: str, user: str = ''):
        """Save data to json"""
        self._json_obj.path = path
        self._json_obj.dict_ = {'transactions': transactions[1]}
        self._json_obj.dump(4)

    def _serialize_to_csv(self, transactions: list, path: str, user: str = ''):
        """Save data to csv"""
        self._csv_obj.header = ['payment', 'payout', 'transaction_name', 'transaction_time',
                                'recipient_name', 'bank_account_number', 'amount']
        self._csv_obj.data = transactions[0]
        self._csv_obj.path = path
        self._csv_obj.write_csv()

    def _serialize_to_pdf(self, transactions: list, path: str, user: str = ''):
        """Save data to pdf"""
        self._pdf_obj.header_text = 'MyBank - Transactions'
        self._pdf_obj.title_text = f'History of the transactions of user {user}'
        self._pdf_obj.body_text = transactions[0]
        self._pdf_obj.add_page()
        self._pdf_obj.print_title()
        self._pdf_obj.print_body()
        self._pdf_obj.output(path)

    @staticmethod
    def create_path(file_path: str, file_name: str, format_: str) -> str:
        """Prepare a path with the filename"""
        return file_path + r'\\' + file_name + '.' + format_

    @staticmethod
    def unpack_data(transactions: list[dict]) -> tuple:
        """Unpack the data and prepare the appropriate structure for saving"""
        list_of_records = []
        list_of_records_dict = []
        for item in transactions:
            item_1 = 'YES' if item.get('payment', 'NO') == 'YES' else 'NO'
            item_2 = 'YES' if item.get('payout', 'NO') == 'YES' else 'NO'
            item_3 = item['transaction_name']
            item_4 = str(item['transaction_time'])
            item_5 = item['recipient_name']
            item_6 = item['bank_account_number']
            item_7 = float(item['amount'])
            list_of_records.append([item_1, item_2, item_3, item_4, item_5, item_6, item_7])
            list_of_records_dict.append({'payment': item_1, 'payout': item_2, 'transaction_name': item_3,
                                         'transaction_time': item_4, 'recipient_name': item_5,
                                         'bank_account_number': item_6, 'amount': item_7})
        return list_of_records, list_of_records_dict
