from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


# Create your views here.
def default(request):
    return render(request, 'default_page/index.html')


def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=login_input)
            username = user_obj.username
        except ObjectDoesNotExist:
            username = login_input

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid credentials')

    return render(request, 'login_page/login.html')


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        if not username:
            if email:
                username = email.split('@')[0]  
            else:
                return f"user_{User.objects.count()+1}"

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists')
            return render(request, 'signup_page/signup.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
    return render(request, 'signup_page/signup.html')

@login_required
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Posted successfully")
            return redirect("home")
        else:
            print("PostForm error:", form.errors)
            messages.error(request, "Could not create post. Check server console for form errors.")
    else:
        form = PostForm()

    posts = Post.objects.all().order_by("-created_at")
    return render(request, 'home_page/home_page.html', {"posts": posts, "form": form})


