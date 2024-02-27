from django.shortcuts import render, redirect
from item.models import Item, Category
from . import forms
# Create your views here.

def index(request):
    Items = Item.objects.all()
    categories = Category.objects.all()
    context = {
        "items" : Items,
        'categories' : categories,
    }
    return render(request, 'core/index.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = forms.SignupForm()

    return render(request, 'core/signup.html', {'form' : form})