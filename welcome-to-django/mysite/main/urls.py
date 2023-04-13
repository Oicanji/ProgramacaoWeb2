from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('todolist/<int:id>', views.getToDoList, name='todolist'),
    path('itemstatuschange/<int:id>', views.itemStatusChange, name='itemstatuschange'),
    path('createnewlist/', views.createNewList, name='createnewlist'),
    path('createnewitem/<int:id>', views.createNewItem, name='createnewitem'),
    path('getitems/<int:id>', views.getItems, name='getitems'),
    path('delitem/<int:id>', views.delItem, name='delitem'),
]