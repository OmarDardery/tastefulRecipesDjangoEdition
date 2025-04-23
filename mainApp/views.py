from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Recipes
from .models import MyUsers
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.http import HttpResponseForbidden
# Create your views here.
def index(request):
    return redirect("login")

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
    stored_usernames = request.COOKIES.get('trdjusernames', '')
    stored_signatures = request.COOKIES.get('trdj_signatures', '')
    print(stored_usernames)
    verified_usernames = []
    signer = TimestampSigner()

    if stored_usernames and stored_signatures:
        try:
            usernames = stored_usernames.split(',')
            signatures = stored_signatures.split(',')

            for username, signature in zip(usernames, signatures):
                try:
                    verified = signer.unsign(signature, max_age=7 * 24 * 60 * 60)
                    if verified == username:
                        verified_usernames.append(username)
                except (SignatureExpired, BadSignature):
                    continue

        except Exception:
            pass
    return render(request, "mainApp/logIn.html", {
        'usernames': verified_usernames
    })
def continueAs(request, username):
    # Get stored signatures
    stored_usernames = request.COOKIES.get('trdjusernames', '').split(',')
    stored_signatures = request.COOKIES.get('trdj_signatures', '').split(',')
    if username not in stored_usernames:
        return HttpResponseForbidden("Username not found in stored credentials")
    signer = TimestampSigner()

    # Find the signature for this username
    try:
        idx = stored_usernames.index(username)
        signature = stored_signatures[idx]

        # Verify signature and check if it's not older than 7 days
        try:
            verified_username = signer.unsign(signature, max_age=7 * 24 * 60 * 60)
            if verified_username == username:
                login(request, MyUsers.objects.get(username=username))
                return redirect('home')
        except (SignatureExpired, BadSignature):
            return HttpResponseForbidden("Invalid or expired signature")

    except ValueError:
        return HttpResponseForbidden("Username not found in stored credentials")

    return HttpResponseForbidden("Authentication failed")

def account(request, action):
    if request.method == 'POST':
        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate() will handle password comparison securely
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                signature = TimestampSigner().sign(username)

                response = redirect('home')

                # Get existing usernames and signatures
                stored_usernames = request.COOKIES.get('trdjusernames', '').split(',') if request.COOKIES.get(
                    'trdjusernames') else []
                stored_signatures = request.COOKIES.get('trdj_signatures', '').split(',') if request.COOKIES.get(
                    'trdj_signatures') else []

                # Add new username and signature if not already present
                if username not in stored_usernames:
                    stored_usernames.append(username)
                    stored_signatures.append(signature)


                # Set cookies with signatures
                response.set_cookie('trdjusernames', ','.join(stored_usernames), max_age=7 * 24 * 60 * 60)
                response.set_cookie('trdj_signatures', ','.join(stored_signatures), max_age=7 * 24 * 60 * 60)

                return response

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
        if request.FILES.get('image'):
            recipe = Recipes.objects.create(
                recipe_id=unique_slug,  # You'll need to generate this
                name=request.POST.get('name'),
                createdBy=request.user.user_id,  # This gets the current user's ID
                description=request.POST.get('description'),
                preparation_time=int(request.POST.get('preparation_time')),
                ingredients=request.POST.get('ingredients'),
                instructions=request.POST.get('instructions'),
                images=request.FILES.get('image')
            )
        else:
            recipe = Recipes.objects.create(
                recipe_id=unique_slug,  # You'll need to generate this
                name=request.POST.get('name'),
                createdBy=request.user.user_id,  # This gets the current user's ID
                description=request.POST.get('description'),
                preparation_time=int(request.POST.get('preparation_time')),
                ingredients=request.POST.get('ingredients'),
                instructions=request.POST.get('instructions'),
            )
        return redirect('recipe-details', recipe_id=recipe.recipe_id)

    return render(request, "mainApp/home.html")
