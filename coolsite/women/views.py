from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import *
from .models import *
from .utils import *

""" Что делаем с menu
    Здесь у нас есть переменная со списком меню(menu) которую мы передаем в качестве словаря 
    в функциях отображения страницы и title в качестве значения той переменной которая указана 
    в файлах html там в свою очередь мы с помощью синтаксиса jinja проходимся по меню и отображаем 
    на странице этот список

    # menu = [{"title": 'Обсайт', "url_name": "about"},
    #         {"title": 'Добавить статью', "url_name": "add_page"},
    #         {"title": 'ОбрСвязь', "url_name": "contact"},
    #         {"title": 'Войти', "url_name": "login"}
    #         ] (меню вынесено в тег templatestag)
"""

""" Словари в функциях                                         
    в этих словарях передаются переменные как значения а ключами
    выступают названия полей используемые в html файле[]
"""

# Функция переписана в класс
# def index(request):
#     """ В функции
#         В функции index переменной posts присваевается ORM запрос
#         из sql таблицы БД в которой у нас внесены данные и этой переменной
#         присваивается вся таблица которая затем передается через
#         словарь в рендер html файла главной страницы и там парсится
#     """
#     posts = Women.objects.all()
#     context = {
#         'posts': posts,
#         'title': 'Главная',
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)


class WomenHome(DataMixin, ListView):
    """
        Класс представления вместо функции указываем в нем модель прописываем 
        где находится нужная html страница для передачи в нее данных и передаем 
        название переменной для итератора (по умолчанию это object_list мы 
        прописываем posts) что бы было понятней и на html странице так же используем posts
    """
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
            Функция формирует динамический контент забирает его у базового класа через супер
            и добавляет по ключу context["title"] = ... данные которые так же необходимо
            передать на html страницу
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        # context["title"] = 'Главная страница'
        # context["cat_selected"] = 0
        return dict(list(context.items()) + list(c_def.items())) #context

    def get_queryset(self):
        """
            Функция возвращает данные таблицы отфильтрованные по флагу публикации
        """
        return Women.objects.filter(is_published=True)


def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj' : page_obj , 'title': 'Обсайт'})

# Функция переписана в класс
# def addpage(request):
#     """ Логика if
#         Логика if определяет что если форма открыта в первый раз то она будет пустой
#         Если форма была частично заполнена значит была нажата кнопка "добавить" и
#         request содержит метод post который мы указали в html файле addpage.html
#         соответственно далее логика пытается сохранить новую запись в бд и в случае
#         ошибки выкинет исключение но оставит форму заполненной тк возьмет данные из
#         ранее заполненной формы благодаря конструкции form = AddPostForm(request.POST)
#     """
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = ('home')
    login_url = ('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
            Функция формирует динамический контент забирает его у базового класа через супер
            и добавляет по ключу context["title"] = ... данные которые так же необходимо
            передать на html страницу
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Добавление статьи')
        #context["title"] = 'Добавление статьи'
        return dict(list(context.items()) + list(c_def.items())) #context

def contact(request):
    return HttpResponse("ОбрСвязь")


def login(request):
    template_name = 'admin'
    #return render(request, 'admin')

# Функция переписана в класс
# def show_post(request, post_slug):
#     """ Функция get_object_or_404
#         Функция get_object_or_404 отображает запись из базы данных таблицы Women
#         с slug=post_slug который передается в запросе или генерит 404 ошибку
#     """
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.slug,
#     }
#     return render(request, 'women/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
            Функция формирует динамический контент забирает его у базового класа через супер
            и добавляет по ключу context["title"] = ... данные которые так же необходимо
            передать на html страницу
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = context["post"])
        #context["title"] = context["post"]
        return dict(list(context.items()) + list(c_def.items())) #context
# Функция переписана в класс представления
# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)

#     if len(posts) == 0:
#         raise Http404

#     context = {
#         'posts': posts,
#         'title': 'Рубрики',
#         'cat_selected': cat_slug
#     }
#     return render(request, 'women/index.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        """
            фильтруем отображаемые посты по категориям. Двойное подчеркивание в
            cat__slug означает что мы обращаемся через FK модели Women к таблице
            Category и фильтруем ее по слагу из выбранной нами категории
        """
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """
            Функция формирует динамический контент забирает его у базового класа через супер
            и добавляет по ключу context["title"] = ... данные которые так же необходимо
            передать на html страницу
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Категория - ' + str(context['posts'][0].cat), cat_selected = context['posts'][0].cat_id)
        # context["title"] = 'Категория - ' + str(context['posts'][0].cat)
        # context["cat_selected"] = context['posts'][0].cat_id
        return dict(list(context.items()) + list(c_def.items())) #context


def categories(reqest, catid):
    """ Catid и Get
        В этой функции так же передается catid для отображения страницы каталога
        если она есть и если была прописана в адресной строке в виде сайт.ру/cats/1
        cats прописывается тк в файле urls.py имя слэга указано именно как cats 
        и далее прописано само название функции которая используется в views
    """
    if (reqest.GET):
        print(reqest.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):
    """ Выражение If
        проверяет не больше ли значение переданное в функцию
        больше текущего года и если да то просто выкидывает на главную страницу
    """
    if int(year) > 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    """
        Функция возвращает надпись вместо 404 отлавливая некорректный ввод в адресной строке
    """
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
