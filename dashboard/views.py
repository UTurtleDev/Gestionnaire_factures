from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def dashboard(request):
    return render(request, 'pages/dashboard/dashboard.html')