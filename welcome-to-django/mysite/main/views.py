from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import  *
from .forms import *

def index(request):
    return HttpResponse("<h1>WELCOME TO DJANGO!!</h1>")

def home(request):
    return render(request, 'main/home.html', {})

def getToDoList(request, id = 0):
    if id == 0:
        return render(request, 'main/home.html', {})
    
    #verify if the id exists
    if not ToDoList.objects.filter(id=id).exists():
        return render(request, 'main/home.html', {})

    todo = ToDoList.objects.get(id=id)

    return render(request, 'main/todolist.html', {"todo": todo})

def itemStatusChange(request, id):
    if not Item.objects.filter(id=id).exists():
        return render(request, 'main/home.html', {})
    
    item = Item.objects.get(id=id)
    item.complete = not item.complete
    item.save()
    return render(request, 'main/todolist.html', {"todo": item.todolist})

def createNewList(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            t = ToDoList(name=name)
            t.save()
        return HttpResponseRedirect('/todolist/%i' % t.id)
    else:
        form = CreateNewList()
    return render(response, 'main/create.html', {"form": form})

def createNewItem(response, id):
    if response.method == "POST":
        form = CreateNewItem(response.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            t = Item(todo=id, text=text, complete=False)
            t.save()
            return HttpResponse("200")
        else:
            return HttpResponse("401")
    else:
        return HttpResponse("404")
    
def getItems(request, id):
    if not ToDoList.objects.filter(id=id).exists():
        return HttpResponse("404")
    
    todo = ToDoList.objects.get(id=id)
    items = Item.objects.filter(todo=todo)
    return HttpResponse(items)

