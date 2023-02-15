# Проект парсинга

Данный проект включает в себя 4 парсера, каждый из которых решает свои задачи.<br>
Парсеры запускаются с помощью соответствующих команд.<br>
В зависимости от выбранного режима, данные парсеров выводятся либо в консоль, либо в csv файл.<br>
Также в работе программы добавлено логирование и обработка ошибок.<br>

### Парсер whats-new

Собирает статьи о нововведениях Python со страницы https://docs.python.org/3/whatsnew/.<br>
Выводит Ссылку на статью, Заголовок статьи и Справочную информацию (имя автора, редактра и т.п.)

Запуск с помощью команды:
```
python main.py whats-new
```

### Парсер latest_versions

Собирает информацию о версияx Python со страницы https://docs.python.org/3/.<br>
Выводит Номера версий, Статусы и Ссылки на документацию.

Запуск с помощью команды:
```
python main.py latest_versions
```

### Парсер downloads

Скачивает архив с документацией Python со страницы https://docs.python.org/3/download.html на локальный диск.

Запуск с помощью команды:
```
python main.py downloads
```

### Парсер pep

Cобирает на странице https://peps.python.org/ документы PEP.<br>
Cравнивает статус документа на странице PEP со статусом документа в общем списке.<br>
Считает кол-во PEP в каждом статусе и общее кол-во PEP.

Запуск с помощью команды:
```
python main.py pep
```

## Другие полезные команды

Вызов справки:
```
python main.py -h
```

Запись данных в файл csv:
```
python main.py pep -o file
```

Вывод данных в консоль с помощью Prettytable:
```
python main.py pep -o pretty
```


## Примеры работы парсера

1. Команда вызова парсера **pep** с выводом в консоль с PrettyTable:
```
python main.py pep -o pretty
```

Ответ в консоли:
```
...
"14.02.2023 12:36:56 - [INFO] - Несовпадающие статусы:
https://peps.python.org/pep-0401
Статус в карточке: April Fool!
Ожидаемые статусы: ('Rejected',)"
+------------+------------+
| Статус     | Количество |
+------------+------------+
| Active     | 31         |
| Withdrawn  | 55         |
| Final      | 269        |
| Superseded | 20         |
| Rejected   | 120        |
| Deferred   | 36         |
| Accepted   | 43         |
| Draft      | 28         |
| Total      | 602        |
+------------+------------+
"14.02.2023 12:36:56 - [INFO] - Парсер завершил работу."
```

2. Команда вызова парсера **latest-versions** без дополнительных режимов:

```
python main.py latest-versions
```

Ответ в консоли:
```
"15.02.2023 15:58:21 - [INFO] - Парсер запущен!"
"15.02.2023 15:58:21 - [INFO] - Аргументы командной строки: Namespace(clear_cache=False, mode='latest-versions', output=None)"
Ссылка на документацию Версия Статус
https://docs.python.org/3.12/ 3.12 in development
https://docs.python.org/3.11/ 3.11 stable
https://docs.python.org/3.10/ 3.10 stable
https://docs.python.org/3.9/ 3.9 security-fixes
https://docs.python.org/3.8/ 3.8 security-fixes
https://docs.python.org/3.7/ 3.7 security-fixes
https://docs.python.org/3.6/ 3.6 EOL
https://docs.python.org/3.5/ 3.5 EOL
https://docs.python.org/2.7/ 2.7 EOL
https://www.python.org/doc/versions/ All versions
"15.02.2023 15:58:22 - [INFO] - Парсер завершил работу."
```

### Разработчик ###

Батова Ольга, студент Яндекс.Практикума
