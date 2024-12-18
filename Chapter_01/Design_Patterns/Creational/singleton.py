import random


class Singleton:
    """Classic singleton"""

    __instance = None

    def __init__(self):
        self.number = random.randint(1, 10)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(Singleton)
        return cls.__instance


class Regular:
    """Simple class to compare behavior"""

    def __init__(self, *args, **kwargs):
        self.number = random.randint(1, 10)


def testing():
    print("Singleton instances")
    list_singleton = [Singleton() for i in range(0, 5)]
    for index, element in enumerate(list_singleton):
        print(f"Element: {index}  number : {element.number}")

    print("Instances of a regular class")
    list_regular = [Regular() for i in range(0, 5)]
    for index, element in enumerate(list_regular):
        print(f"Element: {index}  number : {element.number}")


if __name__ == "__main__":
    testing()
