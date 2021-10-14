from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import User, Item
from .forms import CreationForm

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework import generics, serializers
from .serializers import ItemSerializer, UserSerializer
# Create your views here.


class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUsers(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def create(request):
    if request.method=="POST":
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        form = CreationForm(data=user_data)

        # if form.is_valid():
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        #     newUser = User()
        #     newUser.username = username
        #     newUser.password = password
        #     newUser.save() 
        #     return redirect("/polls/create")
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = CreationForm()
    return render(request, 'create.html', {'form': form})

def createItem(request):
    if request.method=="POST":
        # test
        item_data = JSONParser().parse(request)
        item_serializer = ItemSerializer(data=item_data)

        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)