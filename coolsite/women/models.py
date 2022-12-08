from email.policy import default
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    """
        Здесь в поле photo при его определении мы указываем атрибут
        куда будут загружаться наши фотографии а в саму БД пишется 
        только путь к этим файлам так же там прописано что под каждый день будет создана своя папка
        чтобы джанго понимал куда грузить сами файлы необходимо настроить settings.py в корне проекта
        media_root и media_url
    """
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey(
        'Category', on_delete=models.PROTECT, null=True, verbose_name="Категории")
    '''^
        Назначение столбца Cat внешним ключем для таблицы Category с защитой от удаления
    '''

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        """
            метод возвращает url удобоваримый для path чтобы сформировать 
            ссылку <a href="{{ p.get_abs_url }}"> в index.html
        """
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        """
            метод возвращает url удобоваримый для path чтобы сформировать 
            ссылку <a href="{{ p.get_abs_url }}"> в index.html
        """
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
