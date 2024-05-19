from .exceptions import ContactError
from .fields import Name, Phone, Birthday

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        if self.find_phone(phone):
            raise ContactError("Phone number already exists.")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        existing_phone = self.find_phone(phone)
        if existing_phone:
            self.phones.remove(existing_phone)

    def edit_phone(self, phone: str, new_phone: str):
        existing_phone = self.find_phone(phone)
        if not existing_phone:
            raise ContactError("No such phone number.")

        if self.find_phone(new_phone):
            raise ContactError("New phone number already exists.")

        self.phones[self.phones.index(existing_phone)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        target_phone = Phone(phone)
        return next((p for p in self.phones if p == target_phone), None)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        chunks = []
        chunks.append(f"Contact name: {self.name}")
        chunks.append(f"phones: {'; '.join(p.value for p in self.phones)}")
        if self.birthday:
            chunks.append(f"birthday: {self.birthday.value.strftime('%d.%m.%Y')}")
        return ", ".join(chunks)
