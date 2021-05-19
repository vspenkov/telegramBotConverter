import requests
import json
import datetime
from config import keys, API_access_key, url, TOKEN

d = datetime.datetime.today()
time_format = "%Y-%m-%d %H:%M:%S"

DT = f"{d:{time_format}}"

class ConverterException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price (values):
        if len(values) != 3:
            raise ConverterException("Неверное количество параметров")
        quote, base, amount = values

        if quote == base:
            raise ConverterException("Нельзя осуществить конвертацию конвертируемой валюты")
        try:
            quote_ = keys[quote]
        except KeyError:
            raise ConverterException("Нельзя обработать запрос")

        try:
            base_ = keys[base]
        except KeyError:
            raise ConverterException("Нельзя обработать запрос")

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException ("Нельзя осуществить конвертацию 0")

        r = requests.get(f'{url}?access_key={API_access_key}&symbols={quote_}')
        r1 = requests.get(f'{url}?access_key={API_access_key}&symbols={base_}')

        if base == 'EUR':
            total_base = json.loads(r.content)['rates'][quote_] * amount

        else:
            B = json.loads(r1.content)['rates'][base_]
            A = json.loads(r.content)['rates'][quote_]
            total_base = (B / A) * amount

        return round(total_base, 2)

