from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponseRedirect('Erro no login, contactar')
        else:
            login(request, user)
            return redirect('/')            
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, template_name='../templates/registration/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('/login')
        
        
    
    

   