# Старий інтерфейс
class OldPrinter:
    def print_text(self, text):
        print(f"OldPrinter: {text}")

# Новий інтерфейс
class NewPrinter:
    def print(self, text):
        print(f"NewPrinter: {text}")

# Адаптер
class PrinterAdapter:
    def __init__(self, new_printer: NewPrinter):
        self.new_printer = new_printer

    def print_text(self, text):
        self.new_printer.print(text)

# Використання
def client_code(printer: OldPrinter):
    printer.print_text("Hello, World!")


if __name__ == "__main__":
    # Створення об'єкта нового принтера
    new_printer = NewPrinter()

    # Створення адаптера
    adapter = PrinterAdapter(new_printer)

    # Використання нового принтера через адаптер
    client_code(adapter)
