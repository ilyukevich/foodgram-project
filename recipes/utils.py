from recipes.models import Recipe


def tags_filter(request, author=None, favourites=None):
    """ Filter recipes by tags 'breakfast', 'lunch', 'dinner'"""

    tag_list = ['breakfast', 'lunch', 'dinner']
    tags_for_filter = tag_list.copy()

    for tag_name in tag_list:
        rm_tag = request.GET.get(tag_name)
        if rm_tag:
            tags_for_filter.remove(rm_tag)

    if author:
        recipes = (Recipe.objects
                   .select_related('author')
                   .prefetch_related('recipe_ingredient')
                   .filter(tag__overlap=tags_for_filter, author__username=author))
    elif favourites:
        recipes = (Recipe.objects
                   .select_related('author')
                   .prefetch_related('recipe_ingredient')
                   .filter(tag__overlap=tags_for_filter, favourite__in=favourites))
    else:
        recipes = (Recipe.objects
                   .select_related('author')
                   .prefetch_related('recipe_ingredient')
                   .filter(tag__overlap=tags_for_filter))

    tag = {key: 'tags__checkbox_active' for key in tags_for_filter}

    return recipes, tag
