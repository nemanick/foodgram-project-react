import json
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    help = 'Импорт ингридиентов'

    ingredients_path = os.path.abspath('data/ingredients.json')
    tags_path = os.path.abspath('data/tags.json')

    def handle(self, *args, **kwargs):
        with open(self.ingredients_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for note in data:
            try:
                Ingredient.objects.get_or_create(**note)
                print(f'{note["name"]} записан в базу')
            except Exception as error:
                print(f'Ошибка при добавлении {note["name"]} в базу.\n'
                      f'Ошибка: {error}')

        file.close()

        with open(self.tags_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for note in data:
            try:
                Tag.objects.get_or_create(**note)
                print(f'{note["name"]} записан в базу')
            except Exception as error:
                print(f'Ошибка при добавлении {note["name"]} в базу.\n'
                      f'Ошибка: {error}')

        print('Загрузка успешно завершена!')
