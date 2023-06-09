from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from users.models import Subscribe
from recipes.models import (Favorite, Recipe, RecipeIngredient,
                            ShoppingCart, Ingredient, Tag)
from .filters import AuthorAndTagFilter
from .paginations import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (SubscribeSerializer, TagSerializer,
                          IngredientSerializer, CustomUserSerializer,
                          CustomUserCreateSerializer, RecipeReadSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          FavoriteSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomUserSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(author, context={
                'request': request
            }, data=request.data)
            serializer.is_valid()
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        the_subscribe = get_object_or_404(Subscribe, user=user,
                                          author=author)
        the_subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def subscribtion(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        serializer = SubscribeSerializer(queryset, context={
            'request': request,
        }, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_class = AuthorAndTagFilter
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeReadSerializer
        return RecipeSerializer

    def add_obj(self, request, serializers, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, request, model, id):
        model_instance = model.objects.filter(user=request.user.id,
                                              recipe__id=id)
        if model_instance.exists():
            model_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Такого рецепта нет в списке.'
                         }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_obj(request, FavoriteSerializer, pk)

        return self.delete_obj(request, Favorite, pk)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_obj(request, ShoppingCartSerializer, pk)

        return self.delete_obj(request, ShoppingCart, pk)

    def create_shopping_cart(self, ingredients):
        shopping_list = 'Купить в магазине:'
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['ingredient_value']}")
        file = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_value=Sum('amount'))
        return self.create_shopping_cart(ingredients)
