# Сервис для предсказания значений переменной %target_col_name%
В этом документе представлена документация к сервису для предсказания значений переменной  **%target_col_name%**.  
Json, который необходимо отправить в сервис, выглядит следующим образом:  

```json:
{
    "predict": {
                "data": string
               }
}
```

Data - это свернутый в строку json следующего формата:

```json:
{
%data_part%
}
```

## Структура ответа сервиса
```json:
{
    "state": "OK"
    "prediction": {
                    "prediction": string,
                    "probability": string
                   }
}
```
## Структура ошибки сервиса
```json:
{
    "state": "error",
    "error_log": string
}
```

## Запуск сервиса на localhost:8000
Чтьобы запустить сервис, просто запустите %target_col_name%_service.py    
Это также можно сделать из командной строки при помощи следующей команды:  
```
python predict_%target_col_name%_service.py
```   
## Запуск сервиса с указание хоста и порта
Чтобы запустить сервис, просто запустите %target_col_name%_service.py с двумя параметрами: _host_ and _port_  
Это также можно сделать из командной строки при помощи следующей команды: 
``` 
python predict_%target_col_name%_service.py your_host your_port
``` 
## Использование сервиса из python кода
Чтобы использовать сервис, предсказывающий значения  %target_col_name%, можно использовать следующий код:

```python:
%service_connector%
```
## Телеграм бот для сервиса
Ниже приведен код телеграм бота, который внутри себя использует сервис

```python:
%service_telegram_bot%
```