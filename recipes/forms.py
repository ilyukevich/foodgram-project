from django import forms

from recipes.models import Ingredient, Recipe, RecipeIngredient

from django.core.exceptions import ValidationError

TAGS = [
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
]


class RecipeIngredientForm(forms.ModelForm):
    """Ingredient Form"""

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'ingredient', 'amount')


class RecipeForm(forms.ModelForm):
    """Form for creating a recipe"""

    tag = forms.MultipleChoiceField(
        required=False,
        choices=TAGS,
    )
    time = forms.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'description', 'tag', 'time')

    def __init__(self, *args, **kwargs):
        self.ingredients = []
        self.username = kwargs.pop('username')
        super(RecipeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        check_ing, check_quantity = False, True

        for key, value in self.data.items():
            if key in ['breakfast', 'lunch', 'dinner']:
                cleaned_data['tag'].append(key)
            elif (key.startswith('nameIngredient')
                  or key.startswith('valueIngredient')):
                self.ingredients.append(value)
                check_ing = True

        errors = {}
        if not self.cleaned_data.get('tag'):
            errors['tag'] = ValidationError('Убедитесь, что установили хотя бы один ТЭГ !')

        if errors:
            raise ValidationError(errors)

        if not check_ing:
            raise ValidationError(
                'Проверьте ингридиенты! Добавьте в рецепт хотя бы один ингредиент !'
            )

        for key in self.data.keys():
            if key.startswith('valueIngredient'):
                print(self.data[key])
                if int(self.data[key]) < 1:
                    check_quantity = False

        if not check_quantity:
            raise ValidationError(
                ' Проверьте ингридиенты! Убедитесь, что значения у ингредиентов больше 0 !'
            )

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)
        recipe.author = self.username

        recipe.save()

        for i in range(0, len(self.ingredients), 2):
            ingredient = Ingredient.objects.get(title=self.ingredients[i])
            recipe_ingredient_form = RecipeIngredientForm(
                {
                    'recipe': recipe,
                    'ingredient': ingredient,
                    'amount': self.ingredients[i + 1]
                }
            )
            if recipe_ingredient_form.is_valid():
                recipe_ingredient_form.save()

        return recipe
