from abc import ABC, abstractmethod


class Publisher(ABC):
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class PublisherMessages(Publisher):
    _observers = []
    _indicator = 0

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def business_logic_execution(self):
        print(f"Application logic is being executed. Indicator: {self._indicator}")
        self._indicator += 1
        self.notify()


class Observer(ABC):
    @abstractmethod
    def update(self, publisher):
        pass


class ObserverA(Observer):
    def update(self, publisher):
        if publisher._indicator <= 3:
            print("ObserverA: reacts to the indicator less than 2")


class ObserverB(Observer):
    def update(self, publisher):
        if publisher._indicator > 2:
            print("ObserverB: reacts to the indicator greater than 2")


def client():
    publisher = PublisherMessages()

    observer_a = ObserverA()
    publisher.attach(observer_a)

    observer_b = ObserverB()
    publisher.attach(observer_b)

    publisher.business_logic_execution()
    publisher.business_logic_execution()
    publisher.detach(observer_a)
    publisher.business_logic_execution()


if __name__ == "__main__":
    client()
