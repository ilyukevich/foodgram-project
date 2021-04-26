from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Recipe, ShoppingList
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient"""

    class Meta:
        fields = '__all__'
        model = Ingredient


class ShoppingListSerializer(serializers.ModelSerializer):
    """Serializer for shopping list"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        fields = '__all__'
        model = ShoppingList


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for favorite"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        fields = '__all__'
        model = Favorite


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for follow"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Follow
