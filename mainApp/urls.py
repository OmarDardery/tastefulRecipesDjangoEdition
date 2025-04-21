from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe-details/<slug:recipe_id>", views.recipe_details, name="recipe-details"),
]