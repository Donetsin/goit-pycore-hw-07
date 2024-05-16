'''this module provides OOP model of the note helper'''
import re
from collections import UserDict
from datetime import datetime as dt, timedelta as td

class Field:
    '''documentation for the class Field'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    '''documentation for the class Name'''
    pass

class Phone(Field):
    '''documentation for the class Phone'''
    def __init__(self, value):
        super().__init__(value)
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Error. Phone number must be 10 digits")

class Birthday(Field):
    '''documentation for the class Birthday'''
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            self.value = dt.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")        

    def to_this_year(self) -> dt:
        '''returns Birthday for this year'''
        return self.value.replace(year = dt.now().year)

class Record:
    '''documentation for the class Record'''
    def __init__(self, person_name):
        self.name = Name(person_name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phone(s): {', '.join(number for number in self.phones)}"

    def add_phone(self, phone):
        '''add phone number to record line'''
        self.phones.append(phone)

    def del_phone(self, phone):
        '''delete phone number from record line'''
        self.phones = [number for number in self.phones if number.value != phone]

    def edit_phone(self, old_phone, new_phone):
        '''edit phone number in record line'''
        self.phones = list(map(lambda x: x.replace(old_phone, new_phone), self.phones))

    def find_phone(self, phone):
        '''return phone number from record line'''
        for number in self.phones:
            if number == phone:
                return number
        raise IndexError("Phone number is not found.")

    def add_birthday(self, birthday):
        '''add birthday date to record line'''     
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    '''documentation for the class AddressBook'''
    def add_record(self, record):
        '''add record to address book'''
        self.data[record.name.value] = record

    def find(self, name):
        '''return record from address book'''
        return self.data.get(name)

    def delete(self, name):
        '''delete record from address book'''
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        """Returns list of employee Birthday during next 7 days"""
        current_date = dt.today().date()
        birthdays = []

        for record in self.data.values():
            birthday = record.birthday
            if birthday:
                this_year_birthday = birthday.to_this_year().date()

                # birthday has already passed
                if this_year_birthday < current_date:
                    # use next year birthday
                    this_year_birthday = this_year_birthday.replace(year = current_date.year + 1)

                days_delta = (this_year_birthday - current_date).days
                # check if birthday in next 7 days
                if 0 <= days_delta <= 7:
                    # if Saturday or Sunday
                    if this_year_birthday.weekday() >= 5:
                        # move to Monday
                        this_year_birthday += td(days = 7 - this_year_birthday.weekday())

                    # populate birthday greetings
                    birthdays.append({"name": record.name.value, "congratulation_date": this_year_birthday.strftime("%d.%m.%Y")})

        line = [f"name: {bd['name']},  congratulation date: {bd['congratulation_date']}" for bd in birthdays]
        print(*line, sep = "\n")

# # Створення нової адресної книги
# book = AddressBook()

# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_birthday("18.05.1980")
# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_birthday("20.05.1985")
# book.add_record(jane_record)

# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
# #book.delete("Jane")

# # отримання списку для привітання
# book.get_upcoming_birthdays()
