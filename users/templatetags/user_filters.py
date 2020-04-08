from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})

# синтаксис @register... , под которой описан класс addclass() - 
# это применение "декораторов", функций, обрабатывающих функции
# мы скоро про них расскажем. Не бойтесь соб@к


@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={"class": css})
@register.filter(name='rupluralize')
def rupluralize(value, arg="комментарий,комментария,комментариев"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]