from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
import uuid

# Create your models here.
class Recipes(models.Model):
    recipe_id = models.SlugField(primary_key=True)
    name = models.CharField(max_length=100)
    createdBy = models.UUIDField(editable=False, default=123)
    description = models.TextField()
    preparation_time = models.IntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()
    images = CloudinaryField('image', null=True, blank=True)


class MyUsers(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='myusers_set',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='myusers_set',
        help_text='Specific permissions for this user.'
    )


