from datetime import datetime
from models import Transaction, TransactionManager
from validations import TransactionValidator


class TransactionController:
    """Обрабатывает вводимые пользователем данные c помощью методов класса TransactionManager"""
    def __init__(self):
        self.transaction_manager = TransactionManager()

    def view_balance(self):
        """Вывод текущего баланса, суммы доходов и суммы расходов"""
        total_balance = self.transaction_manager.get_total_balance()
        total_income = self.transaction_manager.get_income()
        total_expenses = self.transaction_manager.get_expenses()

        print(f"\n$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Баланс: {total_balance:.2f}")
        print(f"Сумма доходов: {total_income:.2f}")
        print(f"Сумма расходов: {total_expenses:.2f}")
        print("$$$$$$$$$$$$$$$$$$$$$$$$")

    def add_transaction(self):
        """Добавление новой записи (с валидацией вводимых данных)"""
        while True:
            date_str = input("Введите дату записи (YYYY-MM-DD): ")
            try:
                date = TransactionValidator.validate_date(date_str)
                break
            except ValueError as e:
                print(e)

        while True:
            category = input("Выберете категорию (Доход/Расход): ")
            try:
                category = TransactionValidator.validate_category(category)
                break
            except ValueError as e:
                print(e)

        while True:
            amount = float(input("Введите сумму: "))
            try:
                amount = TransactionValidator.validate_amount(amount)
                break
            except ValueError as e:
                print(e)

        while True:
            description = input("Введите описание: ")
            try:
                description = TransactionValidator.validate_description(description)
                break
            except ValueError as e:
                print(e)

        transaction = Transaction(date, category, amount, description)
        self.transaction_manager.add_transaction(transaction)
        print("\nЗапись успешно добавлена!")
        self.transaction_manager.save_data()

    def search_transactions(self):
        """Поиск записей по переданным критериям (с валидацией)"""
        category = input("Выберете категорию (или пропустите для вывода всех категорий): ")

        date_str = input("Выберете дату (YYYY-MM-DD, или пропустите для вывода записей с любыми датами): ")

        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        amount_str = input("Выберете сумму (или пропустите для вывода записей с любыми суммами): ")

        filtered_transactions = self.transaction_manager.search_transactions(category, date, amount_str)
        return filtered_transactions

    def edit_transaction(self):
        """Редактирование выбранной по критериям записи"""
        transactions = self.search_transactions()
        if not transactions:
            print("Не выбрана ни одна запись. Попробуйте сделать другой запрос.")
            return

        print("\nВыбранным критериям соответствуют следующие записи:\n")
        for i, transaction in enumerate(transactions):
            print(f"{i}. {transaction}")

        while True:
            try:
                index = int(input("\nВведите номер записи для редактирования: "))
                if index < 0 or index >= len(transactions):
                    raise ValueError("Неверный индекс")
                break
            except ValueError as e:
                print(e)
        original_transaction = transactions[index]

        while True:
            date_str = input(f"Введите новую дату (YYYY-MM-DD) [{original_transaction.date.strftime('%Y-%m-%d')}]: ")
            try:
                new_date = TransactionValidator.validate_date(date_str) if date_str else original_transaction.date
                break
            except ValueError as e:
                print(e)

        while True:
            new_category = input(f"Введите новую категорию (Доход/Расход) [{original_transaction.category}]: ")
            try:
                new_category = TransactionValidator.validate_category(new_category) if new_category else original_transaction.category
                break
            except ValueError as e:
                print(e)

        while True:
            amount_str = input(f"Введите новую сумму [{original_transaction.amount}]: ")
            try:
                new_amount = TransactionValidator.validate_amount(amount_str) if amount_str else original_transaction.amount
                break
            except ValueError as e:
                print(e)

        while True:
            new_description = input(f"Введите новое описание [{original_transaction.description}]: ")
            try:
                new_description = TransactionValidator.validate_description(new_description) if new_description else original_transaction.description
                break
            except ValueError as e:
                print(e)

        new_transaction = Transaction(new_date, new_category, float(new_amount), new_description)
        self.transaction_manager.edit_transaction(index, new_transaction)
        self.transaction_manager.save_data()
        print(f"\nЗапись успешно отредактирована:\n{new_transaction}")
        self.transaction_manager.save_data()

