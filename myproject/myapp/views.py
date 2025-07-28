from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')

def pacific(request):
    return render(request, 'myapp/pacificstar/aurora.html')

def podium(request):
    return render(request, 'myapp/podium/bistro.html')
def pacific2(request):
    return render(request, 'myapp/pacificstar/aurora2.html')
def podium2(request):
    return render(request, 'myapp/podium/bistro2.html')

def about(request):
    return render(request, 'myapp/pacificstar/about.html')
def reserve(request):
    return render(request, 'myapp/pacificstar/gallery.html')