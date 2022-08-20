from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='components',
            field=models.ManyToManyField(related_name='recipes', through='recipes.Component', to='recipes.Product', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_product_unit'),
        ),
        migrations.AddField(
            model_name='favourrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite', to='recipes.recipe', verbose_name='Избранные рецепты'),
        ),
        migrations.AddField(
            model_name='favourrecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favour_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Владелец списка избранного'),
        ),
        migrations.AddField(
            model_name='component',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='recipes.product', verbose_name='Ингридиент для рецепта'),
        ),
        migrations.AddField(
            model_name='component',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_components', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='basket',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_recipes', to='recipes.recipe', verbose_name='Рецепты в списке покупок'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL, verbose_name='Список покупок'),
        ),
        migrations.AddConstraint(
            model_name='favourrecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_favour'),
        ),
    ]
