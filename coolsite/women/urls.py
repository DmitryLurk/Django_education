from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("about/", about, name="about"),
    path("addpage/", addpage, name="add_page"),
    path("contact/", contact, name="contact"),
    path("login/", login, name="login"),
    path("post/<slug:post_slug>/", show_post, name="post"),
    path("category/<slug:cat_slug>/", show_category, name="category"),
    path("cats/<int:catid>/", categories),
    re_path(r"^archive/(?P<year>[0-9]{4})", archive),
]
""" Почему /int и r строка
    здесь прописывается что int принемается в качестве аргумента и учавствует в формировании
    render в функции если он присутствует в запросе адресной строки
    rстрока работает аналогично cats только в () прописано что принимается год цифрами [0-9] 
    количество цифр в году должно быть {4}
"""
