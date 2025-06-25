from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')

def pacific(request):
    return render(request, 'myapp/pacificstar/aurora.html')

def podium(request):
    return render(request, 'myapp/podium/bistro.html')
