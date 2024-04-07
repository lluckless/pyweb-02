from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Input error: {e}"
    return wrapper

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @Field.value.setter
    def value(self, new_value):
        if not self.is_valid_phone(new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value    
    
    def is_valid_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()

class Birthdays(Field):
    def __init__(self, value):
        try:
            self.value = dtdt.strptime(value, "%d-%m-%Y").date()    
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        try:
            dtdt.strptime(new_value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self._value = new_value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.value = Birthdays(value)
    
    @input_error
    def add_contact(args, book):
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
    def add_birthday(args, book):
        name, birthday = args
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday added for {name}."
        else:
            return "Contact not found."

    @input_error
    def show_birthday(args, book):
        name = args[0]
        record = book.find(name)
        if record and record.birthday:
            return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
        elif record:
            return f"{name} has no birthday set."
        else:
            return "Contact not found."

    @input_error
    def birthdays(args, book):
        upcoming_birthdays = []
        today = dt.date.today()
        next_week = today + dt.timedelta(days=7)
        for record in book.records:
            if record.birthday:
                if today < record.birthday.value.date() < next_week:
                    upcoming_birthdays.append((record.name.value, record.birthday.value.strftime('%d.%m.%Y')))
        if upcoming_birthdays:
            return "\n".join([f"{name}'s birthday on {date}" for name, date in upcoming_birthdays])
        else:
            return "No upcoming birthdays in the next week."

    #Реалізація методу додавання телефону
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    #Реалізація методу видалення телефону
    def remove_phone(self, phone):
        putin = self.find_phone(phone)
        if putin in self.phones:
            self.phones.remove(putin)
    
    #Реалізація методу редагування телефону
    def change_contact(self, old_phone, new_phone):
        getmanb = self.find_phone(old_phone) 
        self.phones[self.phones.index(getmanb)] = Phone(new_phone)
    
    #Реалізація методу пошуку телефону
    def find_phone(self, phone):
        for pho in self.phones:
            if phone == pho.value:
                return pho
        return None
       
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    #Реалізація методу додавання до data
    def add_record(self, record):
        self.data[record.name.value] = record
    #Реалізація методу пошуку телефону за ім'ям in data
    def find(self, name):
        return self.data[name]

    #Реалізація методу видалення з data
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    
def parse_input(user_input):                     
    cmd, *args = user_input.split()              # Розділяє строку по пробілу на команду і аргументи
    cmd = cmd.strip().lower()                    # Видаляє зайві пробіли і приводить до нижнього реєстру
    return cmd, *args

def add_contact(args, book: AddressBook):                 
    name, phone, *_ = args

    if name not in book:  # Перевіряємо, чи існує контакт з таким ім'ям у книзі
        record = Record(name)
        book.add_record(record)
        print("Contact added.")
    else:
        record = book.find(name)
        print("Contact updated.")

    if phone:
        record.add_phone(phone)
    return "Operation completed successfully."

def show_phone(args, book: AddressBook):                  
    if args:  # Перевіряємо, чи список args не порожній
        name = args[0]  # Присвоюємо значення за індексом
        if name in book:
            return book[name]
        return 'Not found'
    else:
        return 'No arguments provided.'

def show_all_contacts(contacts):                  
    if contacts:                                 
        for name, phone in contacts.items():     # Цикл виводу значень 
            print(f"{name}: {phone}")
    else:
        print("No contacts found.")            

def change_contact(args, book: AddressBook):
    if args:  # Перевіряємо, чи список args не порожній
        name, old_phone, new_phone = args
        if name in book:
            record = book.find(name)
            if record:
                record.change_contact(old_phone, new_phone)
                return f"Contact {name}'s phone number changed from {old_phone} to {new_phone}."
            else:
                return "Contact not found."
        else:
            return f"Contact '{name}' not found in the address book."
    else:
        return 'No arguments provided.'

def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return "Contact not found."

def show_birthday(args, book: AddressBook):
    if args:  # Перевіряємо, чи список args не порожній
        name = args[0]
        record = book.find(name)
        if record:
            birthday = record.birthday
            if birthday:
                return f"{name}'s birthday: {birthday.value.strftime('%d.%m.%Y')}"
            else:
                return f"{name} has no birthday set."
        else:
            return "Contact not found."
    else:
        return 'No arguments provided.'

def birthdays(args, book: AddressBook):
    upcoming_birthdays = []
    today = dt.date.today()
    next_week = today + dt.timedelta(days=7)
    
    for record_name, record in book.items():
        if record.birthday:
            if today < record.birthday.value < next_week:
                upcoming_birthdays.append((record_name, record.birthday.value.strftime('%d.%m.%Y')))
                
    if upcoming_birthdays:
        return "\n".join([f"{name}'s birthday on {date}" for name, date in upcoming_birthdays])
    else:
        return "No upcoming birthdays in the next week."

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            show_all_contacts(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
    
    save_data(book)
if __name__ == "__main__":
    main()