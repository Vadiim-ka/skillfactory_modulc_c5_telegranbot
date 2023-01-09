import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать колличество {amount} !')

        r = requests.get(
            f'https://api.apilayer.com/exchangerates_data/latest?base={base_key}&base=symbols={quote_key}&apikey=qahFlLLuMBymUCeIS9j2eoYhggTafgKc')
        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key] * float(amount)
        new_pri = round(new_price, 3)
        text = f"Цена {amount} {base} в {quote} : {new_pri}"
        return text
