from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'Р',
    'usd': '$',
}
black_words = ["чеснок", "редиска", "war"]


@register.filter()
def currency(value, code='rub'):
    """
   value: значение, к которому нужно применить фильтр
   """

    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value}{postfix}'


@register.filter()
def censor(value):
    for word in black_words:
        value = value.replace(word[1:], '*' * (len(word) - 1))
    return value
