from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import SignupForm, PostForm, UpdateUserForm, UpdateUserProfileForm, RatingsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Profile, Post, Rating
from .serializers import ProfileSerializer, UserSerializer, PostSerializer

from django.contrib.auth import login, authenticate
import random


# Create your views here.

def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    try:
        posts = Post.objects.all()
        posts = posts[::-1]
        a_post = random.randint(0, len(posts)-1)
        random_post = posts[a_post]
        print(random_post.photo)
    except Post.DoesNotExist:
        posts = None
    return render(request, 'index.html', {'posts': posts, 'form': form, 'random_post': random_post})

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})
