from dataclasses import dataclass
from datetime import datetime, date

from validations import TransactionValidator


@dataclass
class Transaction:
    date: date
    category: str
    amount: float
    description: str

    def __str__(self):
        return f" Дата: {self.date.strftime('%Y-%m-%d')} | Категория: {self.category} | Сумма: {self.amount:.2f} | Описание: {self.description}"


class TransactionManager:
    """Описание методов для работы с классом Transaction"""
    def __init__(self):
        self.transactions = []
        self.load_data()

    def load_data(self):
        """Загрузка записей из файла в качестве экземпляров"""
        try:
            with open('data.txt', 'r') as file:
                transaction_data = file.read().strip().split('\n\n')
                for transaction_block in transaction_data:
                    transaction_lines = transaction_block.split('\n')
                    current_transaction = {}
                    for line in transaction_lines:
                        key, value = line.split(': ', 1)
                        current_transaction[key] = value
                    date = datetime.strptime(current_transaction['Дата'], '%Y-%m-%d').date()
                    category = current_transaction['Категория']
                    amount = float(current_transaction['Сумма'])
                    description = current_transaction['Описание']
                    transaction = Transaction(date, category, amount, description)
                    self.transactions.append(transaction)
        except FileNotFoundError:
            print("Файл не найден. Начнем с чистого листа.")

    def save_data(self):
        """Запись данных в файл"""
        with open('data.txt', 'w') as file:
            for transaction in self.transactions:
                file.write(f"Дата: {transaction.date.strftime('%Y-%m-%d')}\nКатегория: {transaction.category}\nСумма: {transaction.amount:.2f}\nОписание: {transaction.description}\n\n")

    def add_transaction(self, transaction: Transaction):
        """Добавление экземпляра"""
        self.transactions.append(transaction)

    def edit_transaction(self, index: int, transaction: Transaction):
        """Редактирование существующего экземпляра"""
        self.transactions[index] = transaction

    def get_transactions(self) -> list[Transaction]:
        """Возвращение списка экземпляров"""
        return self.transactions

    def get_total_balance(self) -> float:
        """Подсчет баланса"""
        income = sum(t.amount for t in self.transactions if t.category == "Доход")
        expenses = sum(t.amount for t in self.transactions if t.category == "Расход")
        return income - expenses

    def get_income(self) -> float:
        """Подсчет доходов"""
        return sum(t.amount for t in self.transactions if t.category == "Доход")

    def get_expenses(self) -> float:
        """Подсчет расходов"""
        return sum(t.amount for t in self.transactions if t.category == "Расход")

    def search_transactions(self, category: str = None, date: date = None, amount: float = None) -> list[Transaction]:
        """Поиск экземпляра по критериям с валидацией вводимых пользователем данных"""
        filtered_transactions = self.transactions
        if category:
            try:
                category = TransactionValidator.validate_category(category)
                filtered_transactions = [t for t in filtered_transactions if t.category == category]
            except ValueError as e:
                print(f"Error: {e}")
                return []

        if date:
            try:
                date = TransactionValidator.validate_date(date.strftime('%Y-%m-%d'))
                filtered_transactions = [t for t in filtered_transactions if t.date == date]
            except ValueError as e:
                print(f"Error: {e}")
                return []

        if amount:
            try:
                amount = TransactionValidator.validate_amount(str(amount))
                filtered_transactions = [t for t in filtered_transactions if t.amount == amount]
            except ValueError as e:
                print(f"Error: {e}")
                return []

        return filtered_transactions
