from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.EmailBackEnd import EmailBackEnd

def REGISTER(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check the data
        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email are Already Exists !")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request,"Username are Already Exists !")
            return redirect('register')

        #register
        user = User(
            email=email,
            username=username,
            )
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request,'registration/register.html')

def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,username=email,password=password)

        if user != None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email and Password Are Invalid !')
            return redirect('login')
    return None

def LOGOUT(request):
    logout(request)
    return redirect('login')

def PROFILE(request):
    return render(request,'registration/profile.html')

def PROFILEUPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userid = request.user.id

        user = User.objects.get(id=userid)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.username = username

        if password != "" and password != None:
            user.set_password(password)
        user.save()
        messages.success(request,"Profile Updated Successfully !")
        return redirect('profile')
        
    return None
