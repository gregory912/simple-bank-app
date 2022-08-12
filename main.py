from service.user_operations import UserOperations


if __name__ == '__main__':
    try:
        bank_app = UserOperations()
        while True:
            bank_app.call_cycle()
    except Exception as e:
        print(e.args[0])


