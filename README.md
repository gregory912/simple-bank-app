
# Simple bank app

The project simulates bank account management from a terminal

## Features
- Create Bank Account.
- Check that all entered data is correct
- Encrypt the password with bcrypt
- All data are stored in mySQL database
- Checking the balance after logging in
- Deposit & Withdraw Money
- Bank Account Type Support (Individual Account, Business Account) 
- Charging interest depending on the type of bank account
- Calculate monthly payment interest for business accounts
- Charge a regular commission for withdrawals from business accounts
- Charge a commission for payouts for business accounts, after making too many monthly transactions
- Search transactions for a given word
- Get a complete list of transactions on your account
- Save found or all transactions to a JSON, CSV or PDF file

## Prerequisites
Make sure you have the following installed on your computer:
- Python 3.10
- Docker

## Requirements
- whoosh = "2.7.4"
- bcrypt = "3.2.2"
- fpdf2 = "2.5.4"
- inflection = "0.5.1"
- coverage = "6.4"
- mysql-connector-python = "8.0.29"

## Setup
1. Create a database from the docker-compose.yml
```bash
$ docker-compose up -d --build
```
2. Install pipenv on your computer
```bash
$ pip install --user pipenv
```
3. Install the virtual environment from the pipfile
```bash
$ pipenv install --ignore-pipfile
```
4. Enter the virtual environment with the shell command
```bash
$ pipenv shell
```
5. Launch application from the console
```bash
$ python main.py
```

## Tests
1. To run tests, set up in the main application folder and call with discover
```bash
$ python -m unittest discover
```
