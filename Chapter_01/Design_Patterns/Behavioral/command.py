from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class CommandCreateXMLOrder(Command):
    def __init__(self, receiver, text: str) -> None:
        self._receiver = receiver
        self._text = text

    def execute(self) -> None:
        self._receiver.createXMLOrder(self._text)


class CommandSendEmail(Command):
    def __init__(self, receiver, html: str) -> None:
        self._receiver = receiver
        self._html = html

    def execute(self) -> None:
        self._receiver.send_email(self._html)


class Receiver:
    def createXMLOrder(self, text: str) -> None:
        print(f"Create XML order: {text} ")

    def send_email(self, text: str) -> None:
        print(f"Send email: {text} ")


class Invoker:
    def __init__(self) -> None:
        self._on_order = None
        self._on_email = None


    def set_on_order(self, command: Command):
        self._on_order = command

    def set_on_email(self, command: Command):
        self._on_email = command

    def generate_general_order(self) -> None:
        self._on_order.execute()
        self._on_email.execute()


def client():
    invoker = Invoker()
    invoker.set_on_order(CommandSendEmail(Receiver(), "Send email"))
    invoker.set_on_email(CommandCreateXMLOrder(Receiver(), "Save report"))
    invoker.generate_general_order()


if __name__ == "__main__":
    client()
