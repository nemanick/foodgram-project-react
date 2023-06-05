from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth import get_user_model


MIN_NUMBER = 1

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True,
                             validators=[
                                RegexValidator(
                                    regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                    message='Ошибка в HEX коде цвета',
                                )
                             ])
    slug = models.SlugField(max_length=200, unique=True,
                            validators=[
                                RegexValidator(
                                    regex='^[-a-zA-Z0-9_]+$',
                                    message='Ошибка в вводе slug поля',
                                )
                            ])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredients_unique'
            )
        ]

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='recipe/')
    text = models.CharField('Текст', max_length=1024)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredients')
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField('Время приготовления в мин.',
                                       validators=[
                                           MinValueValidator(MIN_NUMBER)
                                           ])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredienttorecipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[
        MinValueValidator(MIN_NUMBER,
                          message='Мин. количество ингредиента - 1')
    ])

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='ingredienttorecipe_unique'
            )
        ]


class FavoriteAndShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s_%(class)s_unique',
            )
        ]


class Favorite(FavoriteAndShoppingCart):

    class Meta(FavoriteAndShoppingCart.Meta):
        default_related_name = 'favorite'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(FavoriteAndShoppingCart):

    class Meta(FavoriteAndShoppingCart.Meta):
        default_related_name = 'shoppingcart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
