from controllers import TransactionController
from views import TransactionView


def main():
    controller = TransactionController()
    view = TransactionView(controller)
    view.run()


if __name__ == "__main__":
    main()
