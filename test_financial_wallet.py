import unittest
from datetime import date
from models import TransactionValidator, TransactionManager, Transaction


class TestTransactionValidator(unittest.TestCase):
    def test_validate_date(self):
        self.assertEqual(TransactionValidator.validate_date("2023-04-15"), date(2023, 4, 15))
        self.assertRaises(ValueError, TransactionValidator.validate_date, "2023-15-04")

    def test_validate_category(self):
        self.assertEqual(TransactionValidator.validate_category("Доход"), "Доход")
        self.assertEqual(TransactionValidator.validate_category("Расход"), "Расход")
        self.assertRaises(ValueError, TransactionValidator.validate_category, "Другое")

    def test_validate_amount(self):
        self.assertEqual(TransactionValidator.validate_amount("100.50"), 100.50)
        self.assertRaises(ValueError, TransactionValidator.validate_amount, "abc")

    def test_validate_description(self):
        self.assertEqual(TransactionValidator.validate_description("Покупка продуктов"), "Покупка продуктов")
        self.assertRaises(ValueError, TransactionValidator.validate_description, "")


class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        self.transaction_manager = TransactionManager()

    def test_get_total_balance(self):
        self.assertEqual(self.transaction_manager.get_total_balance(), 58303.01)

    def test_get_income(self):
        self.assertEqual(self.transaction_manager.get_income(), 70903.00)

    def test_get_expenses(self):
        self.assertEqual(self.transaction_manager.get_expenses(), 12599.99)

    def test_add_transaction(self):
        initial_transaction_count = len(self.transaction_manager.transactions)
        new_transaction = Transaction(date(2023, 4, 15), "Доход", 100000.0, "Зарплата")
        self.transaction_manager.add_transaction(new_transaction)
        self.assertEqual(len(self.transaction_manager.transactions), initial_transaction_count + 1)
        self.assertEqual(self.transaction_manager.transactions[-1], new_transaction)

    def test_edit_transaction(self):
        transaction1 = Transaction("2023-04-15", "Расход", 500.0, "Обед")
        transaction2 = Transaction("2023-04-16", "Доход", 100000.0, "Зарплата")
        self.transaction_manager.add_transaction(transaction1)
        self.transaction_manager.add_transaction(transaction2)

        new_transaction = Transaction("2023-04-15", "Расход", 600.0, "Ужин")
        self.transaction_manager.edit_transaction(0, new_transaction)
        self.assertEqual(self.transaction_manager.transactions[0], new_transaction)

    def test_search_transactions(self):
        transaction1 = Transaction(date(2023, 4, 15), "Расход", 500.0, "Обед")
        transaction2 = Transaction(date(2023, 4, 16), "Доход", 100000.0, "Зарплата")
        transaction3 = Transaction(date(2023, 4, 15), "Расход", 750.0, "Бензин")
        self.transaction_manager.add_transaction(transaction1)
        self.transaction_manager.add_transaction(transaction2)
        self.transaction_manager.add_transaction(transaction3)

        filtered_transactions = self.transaction_manager.search_transactions(category="Расход")
        self.assertEqual(len(filtered_transactions), 8)
        self.assertIn(transaction1, filtered_transactions)
        self.assertIn(transaction3, filtered_transactions)

        filtered_transactions = self.transaction_manager.search_transactions(date=date(2023, 4, 15))
        self.assertEqual(len(filtered_transactions), 2)
        self.assertIn(transaction1, filtered_transactions)
        self.assertIn(transaction3, filtered_transactions)

        filtered_transactions = self.transaction_manager.search_transactions(amount=500.0)
        self.assertEqual(len(filtered_transactions), 1)
        self.assertIn(transaction1, filtered_transactions)
