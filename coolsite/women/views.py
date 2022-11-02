from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

def index(request):
    return HttpResponse("Страница приложения women")

def categories(reqest, catid):
    if (reqest.GET):
        print(reqest.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")