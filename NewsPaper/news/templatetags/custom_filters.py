from django import template
 
register = template.Library()

censor_word = [
    "цензура-слово",
]

@register.filter(name='censor')
def censor(value, arg):
    for word in censor_word:
        value = str(value).replace(word, "*****")

    return str(value)