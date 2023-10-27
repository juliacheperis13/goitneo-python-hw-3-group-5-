from collections import UserDict, defaultdict
from datetime import datetime


class InvalidLengthError(Exception):
    pass


class InvalidFormatError(Exception):
    pass


class InvalidDateFormatError(Exception):
    pass


class InvalidRecordError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value.strftime("%d.%m.%Y"))

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value = datetime.strptime(new_value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidDateFormatError()


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) != 10:
            raise InvalidLengthError()
        elif not new_value.isdigit():
            raise InvalidFormatError()
        else:
            self.__value = new_value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: { '; '.join(p.value for p in self.phones) if len(self.phones) else 'No phones added.'}, birthday: { self.birthday if self.birthday is not None else 'No birthday added.'}"

    def add_phone(self, phone):
        if self.__is_phone_available(phone):
            raise InvalidRecordError('Phone is already added')
        else:
            self.phones.append(Phone(phone))

    def edit_phone(self, current_phone, new_phone):
        index = self.__find_phone_index(current_phone)
        if index is not None:
            self.phones[index] = Phone(new_phone)
        else:
            raise InvalidRecordError('Phone does not exist')

    def find_phone(self, phone):
        if self.__is_phone_available(phone):
            return phone
        else:
            raise InvalidRecordError('Phone does not exist')

    def find_phones(self):
        formatted_phones = []
        for phone in self.phones:
            formatted_phones.append(str(phone))

        return ','.join(formatted_phones)

    def remove_phone(self, phone):
        index = self.__find_phone_index(phone)
        if index is not None:
            del self.phones[index]
        else:
            raise InvalidRecordError('Phone does not exist')

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday

    def __find_phone_index(self, phone):
        return next((i for i, item in enumerate(self.phones) if item.value == phone), None)

    def __is_phone_available(self, phone):
        return self.__find_phone_index(phone) is not None


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name
        self.data[name.value] = record

    def find(self, name):
        if name in self.data:
            record = self.data[name]
            return record
        else:
            raise InvalidRecordError('Contact does not exist')

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise InvalidRecordError('Contact does not exist')

    def get_birthdays_per_week(self):
        users_to_congratulate = defaultdict(list)
        current_date = datetime.today().date()

        for name, record in self.data.items():
            if record.birthday is None:
                continue

            default_week_day = 0
            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=current_date.year)

            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(
                    year=current_date.year + 1)

            delta_days = (birthday_this_year - current_date).days

            if delta_days < 7:
                birthday_day_of_week = birthday_this_year.weekday()
                day_of_week = default_week_day if birthday_day_of_week in [
                    5, 6] else birthday_day_of_week
                users_to_congratulate[day_of_week].append(name)

        return self.__get_formatted_birthdays_list(users_to_congratulate) if len(users_to_congratulate) != 0 else 'No upcoming birthdays.'

    def __get_formatted_birthdays_list(self, users):
        week_days = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }

        formatted_list = []

        for i in range(6):
            if i in users:
                formatted_list.append(
                    f'{week_days[i]}: { ", ".join(users[i])}')

        return '\n'.join(formatted_list)
