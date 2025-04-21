from django.contrib import admin

# Register your models here.
from .models import Recipes, MyUsers
admin.site.register(Recipes)
admin.site.register(MyUsers)