import re
import csv


def main():
    with open("phonebook_raw.csv", encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    sort_name(contacts_list)
    change_phone(contacts_list)
    split_record(contacts_list)

    with open("phonebook.csv", 'w', newline="", encoding='UTF-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


def sort_name(contacts_list):
    pattern = r"^(\w+)?\s?(\w+)?\s?(\w+)?"
    for position, item in enumerate(contacts_list):
        if item[0] == 'lastname':
            continue
        full_name = []
        for c in range(3):
            full_name.append(re.search(pattern, item[c]).groups())

        for count, name in enumerate(full_name):
            for count_low, record in enumerate(name):
                if record is not None:
                    item[count + count_low] = record
        contacts_list[position] = item


def change_phone(contacts_list):
    pattern = r'(\+7|8)?[-\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})'
    pattern_with_added = r'(\+7|8)?[-\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2}).*(\d{4}).*'
    for item in contacts_list:
        if item[0] == 'lastname':
            continue
        if re.search('доб', item[5]) is None:
            item[5] = re.sub(pattern, '+7(\\2)\\3-\\4-\\5', item[5])
        else:
            item[5] = re.sub(pattern_with_added, '+7(\\2)\\3-\\4-\\5 доб.\\6', item[5])


def split_record(contacts_list):
    for first_index in range(len(contacts_list)):
        for next_index in range(first_index + 1, len(contacts_list)):
            if (contacts_list[first_index][0] == contacts_list[next_index][0]) | (contacts_list[next_index][1] ==
                                                                                  contacts_list[first_index][1]):
                for record in range(len(contacts_list[first_index])):
                    if contacts_list[first_index][record] < contacts_list[next_index][record]:
                        contacts_list[first_index][record] = contacts_list[next_index][record]
                contacts_list.pop(next_index)
                break


if __name__ == '__main__':
    main()
