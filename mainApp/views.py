from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Recipes
from .models import MyUsers
# Create your views here.
def index(request):
    return render(request, "mainApp/logIn.html")
def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipes, recipe_id=recipe_id)
    return render(request, "mainApp/recipe.html", {
        "recipe": recipe,
    })
@login_required(login_url='login')
def home(request):
    # Fetch all recipes from the database
    recipes = Recipes.objects.all()
    return render(request, "mainApp/home.html", {
        "recipes": recipes,
    })
def signup(request):
    return render(request, "mainApp/signUp.html")
def logIn(request):
    return render(request, "mainApp/logIn.html")
def account(request, action):
    if request.method == 'POST':
        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate() will handle password comparison securely
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Authentication failed
                return render(request, 'mainApp/login.html', {
                    'error': 'Invalid username or password'
                })

        elif action == 'signup':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            if MyUsers.objects.filter(username=username).exists():
                return render(request, 'mainApp/signup.html', {
                    'error': 'Username already exists'
                })

            # Create new user with hashed password
            user = MyUsers.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Hash the password
            )

            # Log the user in
            login(request, user)
            return redirect('home')
    return render(request, 'mainApp/login.html')

@login_required(login_url='login')  # Redirects to login page if user is not authenticated
def add_recipe(request):
    # Your view logic here
    return render(request, "mainApp/add_recipe.html")

def add_recipe_action(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        base_slug = slugify(name)

        # Ensure unique slug
        unique_slug = base_slug
        num = 1
        while Recipes.objects.filter(recipe_id=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1

        recipe = Recipes.objects.create(
            recipe_id=unique_slug,  # You'll need to generate this
            name=request.POST.get('name'),
            createdBy=request.user.user_id,  # This gets the current user's ID
            description=request.POST.get('description'),
            preparation_time=int(request.POST.get('preparation_time')),
            ingredients=request.POST.get('ingredients'),
            instructions=request.POST.get('instructions')
        )
        return redirect('recipe-details', recipe_id=recipe.recipe_id)

    return render(request, "mainApp/home.html")
