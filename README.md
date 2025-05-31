# Project_1
Приложение для анализа банковских операций
***

### Описание модулей

***

### Установка и использование

***

### Примеры использования

***


#### Результаты работы

***


### Тестирование

- Установите через `Poetry` `Pytest`:

```commandline
poetry add --group dev pytest
``` 

- Установите библиотеку `pytest-cov`:

```commandline
poetry add --group dev pytest-cov
```
- Установите библиотеку `requests`:
```commandline
poetry add requests
```
- Установите библиотеку python-dotenv:
```commandline
poetry add python-dotenv
```
- Установите библиотеку pandas:
```commandline
poetry add pandas
```


- Чтобы запустить тесты с оценкой покрытия, можно воспользоваться следующими командами:  
  `pytest --cov`  — при активированном виртуальном окружении.  
  `poetry run pytest --cov` — через poetry.  
  `pytest --cov=src --cov-report=html` — чтобы сгенерировать отчет о покрытии в HTML-формате.   
  где `src` — пакет c модулями, которые тестируем.   
  Отчёт будет сгенерирован в папке `htmlcov` и храниться в файле с названием `index.html`.

- Oтчёт в HTML будет выглядеть следующим образом:

***


### Документация и ссылки


***
