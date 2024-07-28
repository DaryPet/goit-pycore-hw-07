from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str (self.value)

class Name (Field):
    pass

class Phone (Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format. Use 10 digits.")
        super().__init__(value)

    def validate_phone(self, phone):
        return re.fullmatch(r"\d{10}", phone)
    
class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y" )
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
            
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists.")
    
    def __str__(self):
        phone_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phone: {phone_str}, {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find (self, name):
        return self.data.get(name)

    def delete (self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self, days =7):
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= today + timedelta (days=days):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays


def input_error(func):
    def inner(args, book):
        try:
            return func(args, book)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not all arguments provided"
        except KeyError:
            return "No such contacts."
    return inner


@input_error
def add_contact(args, book: AddressBook):
    # реалізація
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    # реалізація
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError ("No such contact.")

    record.edit_phone(old_phone, new_phone)
    return "Phone number is updated."

@input_error
def show_phone(args, book: AddressBook):
    # реалізація
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError ("No such contact.")
    return f"{name}: {",".join(p.value for p in record.phones)}"


@input_error
def show_all(args, book: AddressBook):
    # реалізація
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthdays(args, book: AddressBook):
    # реалізація
    name, birthday, *_ = args
    record = book.find(name)
    # message = "Contact updated."

    if record is None:
        raise KeyError("No such contact.")

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    # реалізація
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError ("No such contact.")
    if not record.birthday:
        return "No birthday data for this contact."
    return f"{name}: {record.birthday}"

@input_error
def birthdays(args, book):
    # реалізація
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays within the next week"
    return "\n".join(f"{record.name}: {record.birthday}" for record in upcoming)


def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0]
    args = parts[1:]
    return command, args


# TODO:

def main():
    book = AddressBook()
    print ("Welcome to the assistant bot!")
    while True:
        user_input = input("enter a command: ")
        command, args = parse_input(user_input)
    
        if command in ["close", "exit"]:
            print ("Good bye!")
            break

        elif command == "hello":
            print ("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthdays(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()





#     # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# # print(john_record)

#     # Додавання запису John до адресної книги
# book.add_record(john_record)
# # print(book)

# #     # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# # print(jane_record)
# book.add_record(jane_record)

#     # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# #     # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# #     # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# #     # Видалення запису Jane
# book.delete("Jane")

# # print(jane) 