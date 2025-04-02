from django import template
import re

register = template.Library()

censor_sign = '*'

'''Все слова, которые нужно цензурировать, начинаются с верхнего или нижнего регистра. \
   Остальные буквы слов могут быть только в нижнем регистре.'''
@register.filter()
def censor(text):
    try:
        if isinstance(text, str) is False:
            raise TypeError
    except TypeError:
        print("Неверный тип данных. Нужен str.")
    else:
        _text = re.findall(r"[\w+]+|[.,!?;:«»/]", text)
        for k, word in enumerate(_text):
            if all([word[1:].islower() is False,
                    word.isdigit() is False]):
                _text[k] = word[0:1] + censor_sign * (len(word) - 1)
            else:
                continue
        formated_text = re.sub(r" ([.,!?;:»/])", r"\1", " ".join(_text))
        formated_text = re.sub(r"([«/]) ", r"\1", formated_text)
        return formated_text
