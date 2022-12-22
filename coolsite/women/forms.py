from django.core.exceptions import ValidationError
from django import forms
from .models import *

# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок')
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Статья')
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     cat=forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Не выбрано')


class AddPostForm(forms.ModelForm):
    """ Class отвечающий
        Class отвечающий за отображение формы добавления поста наследуется от базового 
        класса forms.ModelForm вместе с конструктором в котором при необходимости можно
        переопределить необходимые поля
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        """ В этом метаклассе
            В этом метаклассе прописывается модель к которой будет привязана форма,
            отображающиеся поля (лучше прописывать явно) и стили отображения
        """
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        """
            Валидатор который проверяет длинну поля формы title
        """
        title = self.cleaned_data["title"]
        if len(title) > 100:
            raise ValidationError("Превышена длинна в 100 символов")
        return title
    