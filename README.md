### Описание

Задание курса «Python QA Engineer» (OTUS)

Тестирование API.  
Цель: Тестирование API сервиса с помощью Python используя библиотеки pytest, requests, json.  

Написать минимум 5 тестов для REST API сервиса: https://dog.ceo/dog-api/.
Как минимум 2 из 5 должны использовать параметризацию.

### Установка

Python3 должен быть уже установлен. 
Затем используем `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```#!bash

pip install -r requirements.txt

```

### Запуск
```#!bash

$ pytest test_api_dog_ceo.py

```