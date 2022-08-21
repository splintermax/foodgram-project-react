﻿from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import ProductSearchFilter, RecipeQueryParamFilter
from api.paginations import PageLimitNumberPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (CustomUserSerializer, ProductSerializer,
                             RecipeReadSerializer, SubscribeSerializer,
                             TagSerializer)
from recipes.models import (Basket, Component, FavourRecipe, Product, Recipe,
                            Tag)
from users.models import CustomUser, Follow


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all().prefetch_related('recipes')
    serializer_class = CustomUserSerializer
    pagination_class = PageLimitNumberPagination
    http_method_names = ('get', 'post', 'delete')
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]'

    @action(
        detail=False, methods=('get', ),
        url_path='subscriptions', url_name='subscriptions',
        permission_classes=(IsAuthenticated, ),
        serializer_class=SubscribeSerializer
    )
    def get_subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=('post', 'delete'),
        url_path='subscribe',
        url_name='make_subscribe',
        permission_classes=(IsAuthenticated, ),
        serializer_class=SubscribeSerializer,
    )
    def add_del_sibscription(self, request, pk=None):
        if request.method == 'POST':
            return self.add_follow(request, pk)
        elif request.method == 'DELETE':
            return self.del_follow(request, pk)
        return None

    def add_follow(self, request, pk=None):
        author = get_object_or_404(CustomUser, pk=pk)
        user = request.user
        if user == author:
            return Response({
                'errors': 'Нельзя подписываться на себя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow, subs = Follow.objects.get_or_create(user=user, author=author)
        if subs:
            serializer = SubscribeSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'errors': 'Вы уже подписаны на этого автора'
        }, status=status.HTTP_400_BAD_REQUEST)

    def del_follow(self, request, pk=None):
        user = request.user
        author = get_object_or_404(CustomUser, pk=pk)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (ProductSearchFilter,)
    search_fields = ('^name',)
    http_method_names = ('get',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    permission_classes = (AuthorOrReadOnly, )
    pagination_class = PageLimitNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = RecipeQueryParamFilter

    def add_or_del_recipe(self, request, pk, database):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            if not database.objects.filter(
                    user=self.request.user,
                    recipe=recipe).exists():
                database.objects.create(
                    user=self.request.user,
                    recipe=recipe)
                serializer = RecipeReadSerializer(recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            if database.objects.filter(
                    user=self.request.user,
                    recipe=recipe).exists():
                database.objects.filter(
                    user=self.request.user,
                    recipe=recipe).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True, methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.add_or_del_recipe(request, pk, FavourRecipe)

    @action(detail=True, methods=('post', 'delete'),)
    def shopping_cart(self, request, pk=None):
        return self.add_or_del_recipe(request, pk, Basket)

    @action(
        detail=False, methods=('get',),
        permission_classes=(IsAuthenticated,),
        url_path='download_shopping_cart', url_name='txt_basket',
    )
    def download_text_file(self, request):
        user = request.user
        if not user.basket.exists():
            return Response({
                'errors': 'Список покупок пуст'
            }, status=status.HTTP_400_BAD_REQUEST)

        basket_components = Component.objects.filter(
            recipe__basket_recipes__user=user
        ).values(
            'product__name',
            'product__measurement_unit'
        ).annotate(quantity=Sum('amount')).order_by('product__name')

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        response.write('Список продуктов к покупке\r\n\r\n')
        for component in basket_components:
            response.write(
                f'* {component["product__name"]} - '
                f'{component["quantity"]} '
                f'{component["product__measurement_unit"]} \r\n'
            )
        return response


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)
    pagination_class = None
