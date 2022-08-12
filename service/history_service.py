from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh.filedb.filestore import RamStorage
from database.model.transaction import Transaction


class SearchTransactions:
    def __init__(self):
        self._schema = Schema(
            id=NUMERIC,
            id_profile=NUMERIC,
            payment=TEXT(stored=True),
            payout=TEXT(stored=True),
            transaction_time=DATETIME(stored=True),
            amount=NUMERIC(stored=True),
            bank_account_number=TEXT(stored=True),
            recipient_name=TEXT(stored=True),
            transaction_name=TEXT(stored=True)
        )
        self.fields = ["payment", "payout", "transaction_time", 'amount',
                       'bank_account_number', 'recipient_name', 'transaction_name']

    def _create_index(self) -> None:
        """Create ram storage index in the memory"""
        self.ix = RamStorage().create_index(self._schema)

    def _add_items(self, data: list[Transaction]) -> None:
        """Add data to SegmentWriter object"""
        writer = self.ix.writer()
        [writer.add_document(**item.__dict__) for item in self.decimal_to_float(data)]
        writer.commit(optimize=True)

    def parser(self, entered_value: str) -> iter:
        """Parse and search for the entered value"""
        return self.ix.searcher().search(MultifieldParser(self.fields, schema=self._schema).parse(entered_value))

    def search_elements(self, data: list[Transaction], entered_value: str) -> None:
        """Perform a search for the entered data and print the results"""
        self._create_index()
        self._add_items(data)
        return self.parser(entered_value)

    @staticmethod
    def print_data(data: list[dict]) -> None:
        """Print data for transactions"""
        for item in data:
            print(f"""
            Payment:             {item.get('payment', 'NO')}
            Payout:              {item.get('payout', 'NO')}
            Transaction name:    {item['transaction_name']}
            Transaction time:    {item['transaction_time']}
            Recipient name:      {item['recipient_name']}
            Bank account number: {item['bank_account_number']}
            Transfer amount:     {item['amount']}
            """)

    @staticmethod
    def decimal_to_float(data: list[Transaction]) -> list[Transaction]:
        """Convert decimal to float."""
        for item in data:
            item.amount = float(item.amount)
        return data
