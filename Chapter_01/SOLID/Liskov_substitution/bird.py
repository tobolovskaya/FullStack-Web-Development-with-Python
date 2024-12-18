from abc import ABC, abstractmethod


class Bird(ABC):
    @abstractmethod
    def move(self):
        pass


class FlyableBird(Bird):
    def move(self):
        self.fly()

    @abstractmethod
    def fly(self):
        pass


class Sparrow(FlyableBird):
    def fly(self):
        print("Sparrow is flying")


class Penguin(Bird):
    def move(self):
        print("Penguin is walking")


def make_bird_move(bird: Bird):
    bird.move()


if __name__ == "__main__":
    # Використання
    birds = [Sparrow(), Penguin()]

    for bird in birds:
        make_bird_move(bird)