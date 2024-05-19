import datetime
import pickle

from collections import UserDict

from .exceptions import ContactError
from .fields import Name
from .record import Record

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        if record.name in self.data:
            raise ContactError("Contact already exists.")

        self.data[record.name] = record

    def find(self, name: str, raise_error: bool = True) -> Record | None:
        name = Name(name)

        if name not in self.data:
            if raise_error:
                raise ContactError("No such contact.")
            return None

        return self.data[name]

    def delete(self, name: str):
        name = Name(name)

        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.date.today()
        upcoming_birthdays = []

        for user in self.data.values():
            if user.birthday is not None:
                # user.birthday.value is already a datetime.date object
                birthday = user.birthday.value
                birthday_this_year = datetime.date(today.year, birthday.month, birthday.day)
                # 7 days including today is 6 days from today
                if today <= birthday_this_year <= (today + datetime.timedelta(days=6)):
                    congratulation_date = birthday_this_year
                    if birthday_this_year.weekday() in (5, 6):
                        congratulation_date = birthday_this_year + \
                            datetime.timedelta(days = 7 - birthday_this_year.weekday())

                    upcoming_birthdays.append(
                        {
                            'name': user.name.value,
                            'congratulation_date': congratulation_date.strftime("%d.%m.%Y"),
                        }
                    )

        return upcoming_birthdays
