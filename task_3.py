import csv
import re
from logger_2 import logger


''' Задание 3 - применить написанный логгер к приложению из любого предыдущего д/з.
Домашнее задание по форматированию тел.справочника с помощью регулярных выражений.

'''


@logger(path='log_file_1')
def read_csv(file_path):
    with open(file_path, encoding="utf-8") as f:
        return list(csv.reader(f, delimiter=","))


@logger(path='log_file_2')
def write_csv(file_path, headers, rows):
    with open(file_path, "w", encoding="utf-8", newline='') as res:
        writer = csv.writer(res, delimiter=',')
        writer.writerow(headers)
        writer.writerows(rows)


@logger(path='log_file_3')
def format_phone_number(phone):
    pattern = re.compile(r'(\+7|8)\s*\(*(\d{3})\)*\s*-*(\d{3})-*(\d{2})-*(\d{2})\s*\(*(доб\.)*\s*(\d*)\)*')
    return pattern.sub(r'+7(\2)\3-\4-\5 \6\7', phone).rstrip()


@logger(path='log_file_4')
def process_contacts(contacts_list):
    headers = contacts_list.pop(0)
    new_list = [' '.join(row[0:3]).split() for row in contacts_list]
    name_dict = {}
    for i in range(len(new_list)):
        new_list[i].extend(contacts_list[i][3:])
        k = tuple(new_list[i][:2])
        name_dict.setdefault(k, []).extend(new_list[i][2:])

    res_list = [[*k, *list(dict.fromkeys(v))] for k, v in name_dict.items()]
    for row in res_list:
        if '@' not in row[-1]:
            if len(row) == 7:
                a = row.pop(6)
                row[4] = a
            row.append('')
        row[5] = format_phone_number(row[5])

    return headers, res_list


def main():
    try:
        contacts_list = read_csv("phonebook_raw.csv")
        headers, processed_contacts = process_contacts(contacts_list)
        write_csv("phonebook.csv", headers, processed_contacts)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
