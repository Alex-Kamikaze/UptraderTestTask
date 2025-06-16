from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse, NoReverseMatch

class Menu(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название меню')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items', verbose_name='Меню')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родительский пункт')
    title = models.CharField(max_length=100, verbose_name='Текст пункта меню')
    url = models.CharField(max_length=255, blank=True, verbose_name='URL (явный)')
    named_url = models.CharField(max_length=100, blank=True, verbose_name='Именованный URL')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.url or '#'
        return self.url or '#'

    def __str__(self):
        return self.title