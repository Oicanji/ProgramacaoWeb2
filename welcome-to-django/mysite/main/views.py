from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
# to import in you environment use: pip -m install django

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
    print(request.POST)
    if request.method == "POST":
        id = request.POST.get("id")
        if not Item.objects.filter(id=id).exists():
            return HttpResponse("404")
        item = Item.objects.get(id=id)
        item.complete = not item.complete
        item.save()
        return HttpResponse("200")
    else:
        return HttpResponse("404")

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
        text = response.POST.get("form")
        if not text:
            return HttpResponse("404")
        if not ToDoList.objects.filter(id=id).exists():
            return HttpResponse("404")
        todo = ToDoList.objects.get(id=id)
        item = Item(todolist=todo, text=text, complete=False)
        item.save()

        return HttpResponse("200")
    else:
        return HttpResponse("404")
    
def getItems(request, id):
    if not ToDoList.objects.filter(id=id).exists():
        return HttpResponse("404")
    items = Item.objects.filter(todolist=id)
    if len(items) == 0:
        return HttpResponse("404")
    json_format = json.dumps([{"id": item.id, "text": item.text, "complete": item.complete} for item in items])
    return HttpResponse(json_format)

def delItem(request, id):
    print(request.POST)
    id = request.POST.get("id")
    if not Item.objects.filter(id=id).exists():
        return HttpResponse("404")
    item = Item.objects.get(id=id)
    item.delete()
    return HttpResponse("200")