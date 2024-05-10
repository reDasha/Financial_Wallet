from datetime import datetime, date


class TransactionValidator:
    """Методы для валидации пользовательского ввода"""

    @staticmethod
    def validate_date(date_str: str) -> date:
        """Проверка на ввод корректной даты и приведение ее к нужному формату"""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Неверный формат даты. Нужен такой: YYYY-MM-DD.")

    @staticmethod
    def validate_category(category: str) -> str:
        """Проверка введенной категории (возможны только варианты 'Доход' и 'Расход') с приведением к нужному формату"""
        valid_categories = ['Доход', 'Расход']
        if category.capitalize() in valid_categories:
            return category.capitalize()
        else:
            raise ValueError("Некорректная категория. Введите 'Доход' или 'Расход'.")

    @staticmethod
    def validate_amount(amount: str) -> float:
        """Проверка введенной суммы с конвертацией ее в тип float"""
        try:
            return float(amount)
        except ValueError:
            raise ValueError("Указана некорректная сумма. Введите число")

    @staticmethod
    def validate_description(description: str) -> str:
        """Проверка наличия описания (не пустая строка)"""
        if description.strip():
            return description.strip()
        else:
            raise ValueError("Запись должна содержать описание.")

