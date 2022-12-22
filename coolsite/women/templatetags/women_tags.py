from django import template
from women.models import *

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(slug=filter)


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('women/menu.html')
def main_menu():
    """
        Включенный (inclusion) тег который передает в созданную html страницу 
        ('women/menu.html') словарь с пунктами меню и ссылками в urls.py. таким
        образом в случае корректировок достаточно их будет изменить в одном месте а
        тег поставить там где необходимо отображать меню т.е. в базовом шаблоне который
        мы расширяем другими страницами
    """
    menu = [{"title": 'Обсайт', "url_name": "about"},
            {"title": 'Добавить статью', "url_name": "add_page"},
            {"title": 'ОбрСвязь', "url_name": "contact"},
            {"title": 'Войти', "url_name": "login"}
            ]
    return {'menu': menu}
