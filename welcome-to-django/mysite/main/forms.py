from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class CreateNewItem(forms.Form):
    todo = forms.CharField(label="ToDo", max_length=300)
    text = forms.CharField(label="Text", max_length=300)
    complete = forms.BooleanField(required=False)