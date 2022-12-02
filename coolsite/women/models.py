from email.policy import default
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models


class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    """
        Здесь в поле photo при его определении мы указываем атрибут
        куда будут загружаться наши фотографии а в саму БД пишется 
        только путь к этим файлам так же там прописано что под каждый день будет создана своя папка
        чтобы джанго понимал куда грузить сами файлы необходимо настроить settings.py в корне проекта
        media_root и media_url
    """
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
