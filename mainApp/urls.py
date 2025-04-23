from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe-details/<slug:recipe_id>", views.recipe_details, name="recipe-details"),
    path("login", views.logIn, name="login"),
    path("signup", views.signup, name="signup"),
    path("account/<str:action>", views.account, name="account"),
    path("home", views.home, name="home"),
    path("add-recipe", views.add_recipe, name="add-recipe"),
    path("add-recipe-action", views.add_recipe_action, name="add-recipe-action"),
    path("continue-as/<str:username>", views.continueAs, name="continue-as"),
]