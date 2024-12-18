class Person:
    def __init__(self, name, zip, city, street):
        self.name = name
        self.zip = zip
        self.city = city
        self.street = street

    def get_address(self):
        return f'{self.zip}, {self.city}, {self.street}'


if __name__ == '__main__':
    person = Person('Olexander', '36007', 'Poltava', 'European, 28')
    print(person.get_address())