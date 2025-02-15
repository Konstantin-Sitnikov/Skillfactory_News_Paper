from django import template

from news.models import Censorship

register = template.Library()

def delete_symbol_l_r(word):
    symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')' '*',"\\", '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
               '@', '[', ']', '^', '_', '`', '{', '|', '}']
    for symbol in symbols:
       word = word.rstrip(symbol).lstrip(symbol)
    return word

def stripping(text):
    word = ''
    for i in text:
        if i.isalpha():
            word += i
    return word.lower()


@register.filter()
def censor(text):
    list_censor = [str(i) for i in Censorship.objects.all()]

    for word in text.split():
        format_word = stripping(word)
        if format_word in list_censor:
            cencore_word = format_word[0] + "*" * (len(word) - 1)
            text = text.replace(delete_symbol_l_r(word), cencore_word)

    return text


def set_list_censor():
    return [str(i) for i in Censorship.objects.all()]


# @register.simple_tag(takes_context=True)
# def url_replace(context, **kwargs):
#    d = context['request'].GET.copy()
#    for k, v in kwargs.items():
#        d[k] = v
#    return d.urlencode()