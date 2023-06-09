import json
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    help = 'Импорт ингридиентов'

    path = os.path.abspath('data/ingredients.json')

    def handle(self, *args, **kwargs):
        with open(self.path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for note in data:
            try:
                Ingredient.objects.get_or_create(**note)
                print(f'{note["name"]} записан в базу')
            except Exception as error:
                print(f'Ошибка при добавлении {note["name"]} в базу.\n'
                      f'Ошибка: {error}')

        print('Загрузка успешно завершена!')
