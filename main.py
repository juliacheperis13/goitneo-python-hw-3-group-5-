from address_book import AddressBook, Record, InvalidLengthError, InvalidFormatError, InvalidDateFormatError, InvalidRecordError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give necessary paramaters please."
        except KeyError as ke:
            return f"Error: {ke}"
        except IndexError:
            return "Give me name please."
        except InvalidLengthError:
            return "Error. Phone number should be 10 characters long."
        except InvalidFormatError:
            return "Error. Phone number should contain only digits."
        except InvalidDateFormatError:
            return "Error. Date format is not correct. Should be DD.MM.YYYY."
        except InvalidRecordError as ie:
            return f"Error. {ie}"
        except:
            return "Something went wrong."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    contact = Record(name)
    contact.add_phone(phone)
    contacts.add_record(contact)
    return "Contact added."


@input_error
def change_contact(args, contacts: AddressBook):
    name, current_phone, new_phone = args
    contact = contacts.find(name)
    contact.edit_phone(current_phone, new_phone)
    return "Contact changed."


@input_error
def show_phone(args, contacts):
    name, phone = args
    contact = contacts.find(name)
    contact.find_phone(phone)
    return f"Phone: {phone}"


@input_error
def show_phones(args, contacts):
    name = args[0]
    contact = contacts.find(name)
    phones = contact.find_phones()
    return f"Phone: {phones}"


@input_error
def show_all(args, contacts):
    if len(contacts) == 0:
        return "No contacts."
    else:
        formatted_contacts = []

        for name, record in contacts.data.items():
            formatted_contacts.append(f'{record}')

        return "\n".join(formatted_contacts)


@input_error
def add_birthday(args, contacts):
    name, birthday = args
    contact = contacts.find(name)
    contact.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, contacts):
    name = args[0]
    contact = contacts.find(name)
    birthday = contact.show_birthday()
    return f"Birthday: {birthday}"


@input_error
def birthdays(args, contacts):
    return contacts.get_birthdays_per_week()


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "phones":
            print(show_phones(args, contacts))
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
