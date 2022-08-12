import csv


class OperationsCSV:
    def __init__(self):
        self.path = str()
        self.header = str()
        self.data = None

    def read_csv(self, delimiter: str = ',') -> list:
        """Read data from csv file"""
        list_ = []
        with open(self.path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            for row in reader:
                list_.append(row)
        return list_

    def read_dict_csv(self) -> list[dict]:
        """Read data as dict from csv file"""
        list_ = []
        with open(self.path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                list_.append(dict(row))
        return list_

    def write_csv(self, mode: str = 'w', newline: str = '', delimiter: str = ',') -> None:
        """Write data to a csv file"""
        with open(self.path, mode, newline=newline) as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(self.header)
            for line in self.data:
                writer.writerow(line)

    def write_csv_mltp_rows(self, mode: str = 'w', newline: str = '', delimiter: str = ',') -> None:
        """Write multiple rows data to a csv file"""
        with open(self.path, mode, newline=newline) as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerows(self.data)

    def write_dict_csv(self, fieldnames: list, mode: str = 'w', newline: str = '') -> None:
        """Write dict data to a csv file"""
        with open(self.path, mode, newline=newline) as file:
            fieldnames_ = fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames_)
            writer.writeheader()
            writer.writerow(self.data)
