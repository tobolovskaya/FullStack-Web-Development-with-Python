class DataProcessor:
    def process_data(self, data):
        # Якась складна обробка даних
        return data.upper()


def test_data_processor(mocker):
    processor = DataProcessor()

    # Створюємо шпигуна для методу process_data
    spy = mocker.spy(processor, "process_data")

    # Викликаємо метод
    result = processor.process_data("hello")

    # Перевіряємо, чи був викликаний метод
    assert spy.called
    # Перевіряємо, скільки разів було викликано метод
    assert spy.call_count == 1
    # Перевіряємо аргументи виклику
    assert spy.call_args == mocker.call("hello")

    # Перевіряємо результат
    assert result == "HELLO"
