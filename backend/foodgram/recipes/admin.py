from django.contrib import admin

from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'cooking_time'
    )
    list_filter = ('author', 'name')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color'
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
