from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>WELCOME TO DJANGO!!</h1>")