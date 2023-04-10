from pprint import pprint
import re
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

## 1. Выполните пункты 1-3 задания.
## Ваш код
# Словарь обработанных строк
contacts_dict = {'head': contacts_list[0]}
# Количество столбцов во входном CSV-файле
columns_amt = len(contacts_dict['head'])
for row in contacts_list[1:]:
  new_row = row
  # Во входном CSV-файле присутствует строка с неверным количеством элементов,
  # поэтому проверяем и при необходимости корректируем количество элементов
  # для исключения ошибки при обработке строки
  new_row_len = len(new_row)
  if new_row_len != columns_amt:
    if new_row_len > columns_amt:
      new_row = new_row[:columns_amt]
    else:
      new_row = new_row + ([''] * (columns_amt - new_row_len))
  
  # Если элемент с Ф, с И или с О пустой, то
  if not new_row[0] or not new_row[1] or not new_row[2]:
    # Объединяем элементы с ФИО в одну строку
    lfs_str = ' '.join(new_row[:3])
    # Разделяем строку с ФИО в список Ф, И, О
    lfs_list = re.split(r'\s+', lfs_str)[:3]
    # Формируем строку с обработанными элементами Ф, И, О
    new_row = lfs_list + new_row[3:]
  # Шаблон для обработки номера телефона
  phone_pattern =\
    r'(\+?[78])\s?\(?(\d{3})\)?\s?-?(\d{3})-?(\d{2})-?(\d{2})((\s).?(доб\.)\s(\d+)\)?)?'
  # Подменяем элемент с номером телефона на отформатированный вариант
  new_row[5] = re.sub(phone_pattern, r'+7(\2)\3-\4-\5\7\8\9', new_row[5])
  # Формируем строку ФИ для использования в качестве ключа в словаре
  lf = ' '.join(new_row[:2])
  # Если ранее уже обрабатывалась строка с таким ФИ, то
  if lf in contacts_dict.keys():
    # Запускаем цикл по элементам начиная с элемента с Отчеством
    for i in range(2, len(new_row)):
      # Если у ранее обработанной строки элемент пустой, то
      if not contacts_dict[lf][i]:
        # Заменяем пустой элемент на элемент обрабатываемой строки
        contacts_dict[lf][i] = new_row[i]
  # Если ранее строка с таким ФИ не обрабатывалась, то
  else:
    # Добавляем строку в словарь обработанных строк
    contacts_dict[lf] = new_row

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  
## Вместо contacts_list подставьте свой список:
  datawriter.writerows(contacts_dict.values())