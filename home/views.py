from django.shortcuts import render
import random

# Create your views here.

def home(request):
    template = 'index.html'
    bg_no=random.randint(5,7)
    context={"bg_no": bg_no}
    return render(request, template, context)