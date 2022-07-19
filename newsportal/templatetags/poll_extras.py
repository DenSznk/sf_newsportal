from django import template
import re

register = template.Library()

bad_words = ['some_bad_word', 'another_bad_word']


# just for test
@register.filter()
def upper(value):
    return value.upper()


@register.filter()
def censor(value):
    censored_value = ' '.join(f"{i[0]}***" if i in bad_words else i for i in value.split())
    return censored_value


