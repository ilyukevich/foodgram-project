from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram_project.settings import COUNT_RECIPE
from recipes.forms import RecipeForm
from recipes.models import (Favorite, Follow, Recipe, RecipeIngredient,
                            ShoppingList)
from recipes.utils import tags_filter
from users.models import User
from django.db.models import F, Sum

from django.conf import settings


def index(request):
    """Index page"""

    shopping_list_ids = None
    favorites_ids = None
    recipes, tag = tags_filter(request)

    paginator = Paginator(recipes, COUNT_RECIPE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if not request.user.is_anonymous:
        user = request.user
        shopping_list_ids = (ShoppingList.objects
                             .filter(user=user)
                             .values_list('recipe', flat=True))
        favorites_ids = (Favorite.objects
                         .filter(user=user)
                         .values_list('recipe', flat=True))

    context = {
        'tag': tag,
        'shopping_list_ids': shopping_list_ids,
        'favorites_ids': favorites_ids,
        'page': page,
        'paginator': paginator
    }

    return render(request, 'index.html', context)


def author_recipes(request, slug):
    """Author's recipes"""

    shopping_list_ids = None
    favorites_ids = None
    followers_ids = None
    recipes, tag = tags_filter(request, author=slug)
    author_id = get_object_or_404(User, username=slug).id

    paginator = Paginator(recipes, COUNT_RECIPE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if not request.user.is_anonymous:
        user = request.user
        shopping_list_ids = (ShoppingList.objects
                             .filter(user=user)
                             .values_list('recipe', flat=True))
        favorites_ids = (Favorite.objects
                         .filter(user=user)
                         .values_list('recipe', flat=True))
        followers_ids = (Follow.objects
                         .filter(user=user)
                         .values_list('author', flat=True))

    context = {
        'tag': tag,
        'shopping_list_ids': shopping_list_ids,
        'favorites_ids': favorites_ids,
        'author': slug,
        'author_id': author_id,
        'followers_ids': followers_ids,
        'page': page,
        'paginator': paginator
    }

    return render(request, 'author_recipes.html', context)


def single_recipe(request, slug):
    """View recipe"""

    favorites_ids = None
    shopping_list_ids = None
    followers_ids = None
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    if not request.user.is_anonymous:
        user = request.user
        favorites_ids = (Favorite.objects
                         .filter(user=user)
                         .values_list('recipe', flat=True))
        shopping_list_ids = (ShoppingList.objects
                             .filter(user=user)
                             .values_list('recipe', flat=True))
        followers_ids = (Follow.objects
                         .filter(user=user)
                         .values_list('author', flat=True))

    context = {
        'recipe': recipe,
        'favorites_ids': favorites_ids,
        'shopping_list_ids': shopping_list_ids,
        'followers_ids': followers_ids,
        'ingredients': ingredients,
    }
    return render(request, 'single_recipe.html', context)


@login_required
def create_recipe(request):
    """Create a recipe"""

    if request.method == 'POST':
        recipe_form = RecipeForm(
            request.POST,
            request.FILES,
            username=request.user
        )
        if recipe_form.is_valid():
            recipe_form.save()

            return redirect('index')
    else:
        recipe_form = RecipeForm(username=request.user)

    user = request.user
    shopping_list_ids = (ShoppingList.objects
                         .filter(user=user)
                         .values_list('recipe', flat=True))
    context = {
        'form': recipe_form,
        'shopping_list_ids': shopping_list_ids,
    }
    return render(request, 'create_recipe.html', context=context)


@login_required
def edit_recipe(request, slug):
    """Edit recipe"""

    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    my_shopping_list = ShoppingList.objects.filter(user=request.user)

    if request.method == 'POST':
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        recipe_form = RecipeForm(
            request.POST,
            request.FILES,
            username=request.user,
            instance=recipe,
        )

        if recipe_form.is_valid():
            recipe_form.save()

            return redirect('index')
    else:
        recipe_form = RecipeForm(username=request.user, instance=recipe)

    context = {
        'form': recipe_form,
        'recipe': recipe,
        'ingredients': ingredients,
        'shopping_list_ids': my_shopping_list,
    }
    return render(request, 'edit_recipe.html', context)


@login_required
def favorites(request):
    """Add in favorites"""

    user = request.user
    favourites = Favorite.objects.filter(user=user)
    if not favourites:
        favourites = [-1]

    recipes, tag = tags_filter(request, favourites=favourites)
    paginator = Paginator(recipes, COUNT_RECIPE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    shopping_list_ids = (ShoppingList.objects
                         .filter(user=user)
                         .values_list('recipe', flat=True))
    favorites_ids = (Favorite.objects
                     .filter(user=user)
                     .values_list('recipe', flat=True))

    context = {
        'tag': tag,
        'shopping_list_ids': shopping_list_ids,
        'favorites_ids': favorites_ids,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'favorite.html', context)


def paginator_data(request, recipes):
    paginator = Paginator(recipes, settings.PAG_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


@login_required
def followers(request):
    """Subscriptions"""

    follow_authors = User.objects.filter(
        following__user=request.user).prefetch_related('recipe')
    page, paginator = paginator_data(request, follow_authors)
    one_list = [1, 21, 31, 41, 51, 61, 71, 81, 91]
    two_list = [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54, 62,
                63, 64, 72, 73, 74, 82, 83, 84, 92, 93, 94]
    three_list = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                  25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 45, 46, 47,
                  48, 49, 50, 55, 56, 57, 58, 59, 60, 65, 66, 67, 68, 69, 70,
                  75, 76, 77, 78, 79, 80, 85, 86, 87, 88, 89, 90, 95, 96, 97,
                  98, 99, 100]
    context = {
        'page': page,
        'paginator': paginator,
        'one_list': one_list,
        'two_list': two_list,
        'three_list': three_list,
    }
    return render(request, 'followers.html', context)


def shopping_list(request):
    """Shopping list"""

    user = request.user
    my_shopping_list = ShoppingList.objects.filter(user=user)
    recipes = Recipe.objects.filter(shopping_list__in=my_shopping_list)

    context = {
        'shopping_list_ids': my_shopping_list,
        'recipes': recipes,
    }
    return render(request, 'shopping_list.html', context=context)


def remove_recipe(request, slug):
    """Remove a recipe"""

    Recipe.objects.filter(slug=slug).delete()
    return redirect('index')


def download_shopping_list(request):
    """Download a shopping list"""

    items = RecipeIngredient.objects.select_related('recipe', 'ingredient')

    if request.user.is_authenticated:
        items = items.filter(recipe__shopping_list__user=request.user)
    else:
        return HttpResponse('Ошибка')

    items = items.values(
        'ingredient__title', 'ingredient__dimension'
    ).annotate(
        name=F('ingredient__title'),
        units=F('ingredient__dimension'),
        total=Sum('amount'),
    ).order_by('-total')

    if items:
        text = '\n'.join([
            f"{item['name']} ({item['units']}) - {item['total']}"
            for item in items
        ])

        filename = "foodgram_shoping_cart.txt"
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    return redirect('index')


def page_not_found(request, exception):
    """404"""

    return render(
        request,
        'errors/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    """500"""

    return render(request, 'errors/500.html', status=500)
