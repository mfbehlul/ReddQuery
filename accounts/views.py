from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def register_view(request):
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,'Account is created for '+ user)
                return redirect('login')
        context={'form':form}
        return render(request,'accounts/oldregister.html',context)


def login_view(request):
        
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request, username=username,password=password)
           

            if user is not None:
                login(request,user)
                #return render(request,'accounts/login.html',datakeyword)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
            
        context={}
        return render(request,'accounts/oldlogin.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')


