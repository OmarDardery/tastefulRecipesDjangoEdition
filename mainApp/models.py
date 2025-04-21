from django.db import models

# Create your models here.
class Recipes(models.Model):
    recipe_id = models.SlugField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    preparation_time = models.IntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()
