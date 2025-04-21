from django.shortcuts import render, get_object_or_404
from .models import Recipes
# Create your views here.
def index(request):
    recipes = Recipes.objects.all()
    print(recipes.values())
    return render(request, "mainApp/index.html", {"recipes": recipes})
def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipes, recipe_id=recipe_id)
    return render(request, "mainApp/recipe.html", {
        "recipe": recipe,
    })