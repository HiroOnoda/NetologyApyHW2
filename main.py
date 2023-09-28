import re
from pprint import pprint
import csv


#Сначала составим полную строку по типу выходной, потом будем удалять дубликаты

phone_pattern = r"(\(*\d+\)*\s*\d+[-\s]*+\d+[-\s]*+\d+)\s*(\s*\(?(доб.\s*\d*)\)?)*"
#phone_add = r"\s*\(?(доб.\s*\d*)\)?"
#phone_pre = r"(\+7|8)\s*"
fio_pattern = r"[А-Я][^А-Я][а-я]*"
orgs_pattern = r"[А-Я]+[а-я]*"
pos_pattern = r"(\D+\s*)"
email_pattern = r"(\w*\@\w*\.[ru|com])"

fixed_list = []

i = 0
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
with open("phonebook_raw.csv",encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


all_lines_unsorted = []


# Цикл внизу откровенно говоря неэффективен и тик писать на питоне скорее всего не очень хорошо
# Но, за счет того что я насорил в цикле для чтения у меня получается практически идеальный список
# из списков длиной в 7 строк, в котором каждый элемент расположен там, где должен находиться в
# строке, которую я буду выгружать в итоговый файл.
# Это на порядок упрощает процесс сортировки входных данных и
# полностью аннулирует проблемы с присвоением, например, нужного телефона человеку с нужным ФИО,
# поэтому я решил сделать его таким.
for row in contacts_list[1:]:
    unsorted_line = []
    unsorted_phones = []
    unsorted_orgs = []
    unsorted_emails = []
    unsorted_pos = []
    phone = ''
    for word in row[:3]:
        fio = re.findall(fio_pattern, word)
        if (len(fio) == 0) and (len(unsorted_line) < 3):
            fio.append('')
        unsorted_line += fio
    for word in row[3:4]:
        unsorted_orgs += (re.findall(orgs_pattern, word))
    orgs = ''.join(unsorted_orgs)
    unsorted_line.append(orgs)
    for word in row[4:5]:
        unsorted_pos += (re.findall(pos_pattern, word))
    pos = ''.join(unsorted_pos)
    unsorted_line.append(pos)
    for word in row[0:]:
        unsorted_phones += (re.findall(phone_pattern, word))
    try:
        unsorted_phones = list(unsorted_phones[0])
        phone = ' '.join((list(unsorted_phones))[0:2])
    except IndexError:
        pass
    unsorted_line.append(phone)
    for word in row[0:]:
        unsorted_emails += ''.join(re.findall(email_pattern, word))
    email = ''.join(unsorted_emails)
    unsorted_line.append(email)
    #print(unsorted_line)
    all_lines_unsorted.append(unsorted_line)
    pass


# Сортировка:

# Исхожу из того, что все фамилии уникальны
for count1, instance1 in enumerate(all_lines_unsorted):
    for count2, instance2 in enumerate(all_lines_unsorted):
        # Если фамилии не уникальны, то
        if (instance1[0] == instance2[0]) and (count1 != count2):
            for i in range(1,7):
                if instance2[i] != '':
                    instance1[i] = instance2[i]
            del all_lines_unsorted[count2]
        pass
    pass

with open("fixed_phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(all_lines_unsorted)

pprint(all_lines_unsorted)

#Старая ф-ция для сортировки массива из прошлой попытки, в финальной версии уже не актуальна
# name_sorter = list()
# unsorted_names = list(filter(None, unsorted_names))
# for count, instance in enumerate(unsorted_names):
#     if len(name_sorter) <= i:
#         name_sorter.append([])
#     # Почему он равняет длину пустого листа сначала к 0 а потом к 3
#     elif len(name_sorter[i]) == 3:
#         i += 1
#         name_sorter.append([])
#     if (len(name_sorter[i]) + len(instance)) <= 3:
#         name_sorter[i].extend(instance)
