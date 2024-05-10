def display_menu():
    """Функция для вывода меню в консоль"""
    print("\n===== Личный финансовый кошелек =====")
    print("1. Вывести баланс")
    print("2. Добавить запись")
    print("3. Редактировать запись")
    print("4. Поиск по записям")
    print("5. Выход")


class TransactionView:
    """Класс для описания работы интерфейса консольного приложения"""
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        """Выбор варианта запускается в цикле, который завершается с выбором цифры 5"""
        while True:
            display_menu()
            choice = input("Введите номер задачи: ")

            if choice == '1':
                self.controller.view_balance()
            elif choice == '2':
                self.controller.add_transaction()
            elif choice == '3':
                self.controller.edit_transaction()
            elif choice == '4':
                filtered_transactions = self.controller.search_transactions()
                for transaction in filtered_transactions:
                    print(transaction)
            elif choice == '5':
                print("\n До встречи!\n")
                break
            else:
                print("\nЯ вас не понимаю. Давайте попробуем еще раз!")
