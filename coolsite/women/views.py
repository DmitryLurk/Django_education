from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import *
"""Что делаем с menu
Здесь у нас есть переменная со списком меню(menu) которую мы передаем в качестве словаря 
в функциях отображения страницы и title в качестве значения той переменной которая указана 
в файлах html там в свою очередь мы с помощью синтаксиса jinja проходимся по меню и отображаем 
на странице этот список
"""
menu = [{"title": 'Обсайт', "url_name": "about"},
        {"title": 'Добавить статью', "url_name": "add_page"},
        {"title": 'ОбрСвязь', "url_name": "contact"},
        {"title": 'Войти', "url_name": "login"}
        ]
"""
    В функции index переменной posts присваевается ORM запрос 
    из sql таблицы БД в которой у нас внесены данные и этой переменной присваивается вся таблица
    которая затем передается через словарь в рендер html файла 
    главной страницы и там парсится в список
"""


def index(request):
    posts = Women.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная',
        'cat_selected': 0
    }
    return render(request, 'women/index.html', context=context)


"""Словари в функциях                                         
                                            в этих словарях передаются переменные 
                                            как значения а ключами выступают названия 
                                            полей используемые в html файле[]                                              

"""


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'Обсайт'})


def addpage(request):
    return HttpResponse("ДобСтат")


def contact(request):
    return HttpResponse("ОбрСвязь")


def login(request):
    return HttpResponse("Ку")


def show_post(request, post_id):
    return HttpResponse(f"Статья {post_id}")


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)

    if len(posts) == 0:
        raise Http404

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Рубрики',
        'cat_selected': cat_id
    }
    return render(request, 'women/index.html', context=context)


def categories(reqest, catid):
    """Catid и Get
        В этой функции так же передается catid для отображения страницы каталога
        если она есть и если была прописана в адресной строке в виде сайт.ру/cats/1
        cats прописывается тк в файле urls.py имя слэга указано именно как cats 
        и далее прописано само название функции которая используется в views
    """
    if (reqest.GET):
        print(reqest.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):
    """Выражение If
        проверяет не больше ли значение переданное в функцию
        больше текущего года и если да то просто выкидывает на главную страницу
    """
    if int(year) > 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    """
        Функция возвращает надпись вместо 404 отлавливая некорректный воод в адресной строке
    """
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
