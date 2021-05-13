from django.shortcuts import render

# Create your views here.
def tour_search(request):
    context={
        
    }
    template ='search.html'
    return render(request, template, context)