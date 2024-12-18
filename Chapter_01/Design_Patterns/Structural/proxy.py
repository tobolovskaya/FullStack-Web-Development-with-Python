from abc import ABC, abstractmethod
from time import time, sleep

class Request(ABC):
    @abstractmethod
    def request(self) -> None:
        pass


class RealRequest(Request):
    def request(self) -> None:
        print("RealRequest: Handling request.")
        sleep(0.5)


class Proxy(Request):
    def __init__(self, real_request) -> None:
        self._real_request = real_request
        self.start = None

    def request(self) -> None:
        self.start = time()
        self._real_request.request()
        self.log_access()

    def log_access(self) -> None:
        print(f"Proxy: Logging the time of request. {time() - self.start}")


def client_code(subject) -> None:
    subject.request()


if __name__ == "__main__":
    proxy = Proxy(RealRequest())
    client_code(proxy)