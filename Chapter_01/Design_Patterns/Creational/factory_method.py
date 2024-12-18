from abc import ABC, abstractmethod


class Creator(ABC):
    @abstractmethod
    def create(self):
        pass

    def send_messages(self) -> str:
        product = self.create()
        result = product.sending()
        return result


class SendingMessages(ABC):
    @abstractmethod
    def sending(self) -> str:
        pass


class CreatorPush(Creator):
    def create(self) -> SendingMessages:
        return SendingPushMessages()


class CreatorSMS(Creator):
    def create(self) -> SendingMessages:
        return SendingSMSMessages()


class SendingPushMessages(SendingMessages):
    def sending(self) -> str:
        return "Push mailing has been completed"


class SendingSMSMessages(SendingMessages):
    def sending(self) -> str:
        return "SMS mailing has been completed"


def client_code(creator: Creator) -> None:
    print("We know nothing about the creator code that works")
    result = creator.send_messages()
    print(f"Result: {result}")


if __name__ == "__main__":
    print("The application performs Push mailing lists.")
    client_code(CreatorPush())
    print("\n")

    print("The application performs SMS mailing.")
    client_code(CreatorSMS())