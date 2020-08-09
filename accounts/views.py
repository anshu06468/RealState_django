from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from contacts.models import Contacts
from django.contrib import messages,auth

# Create your views here.
def register(request):
    if request.method == 'POST':
        #Register
        firstname=request.POST["first_name"]
        lastname=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        password2=request.POST["password2"]

        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email is being Used')
                    return redirect('register')
                else:
                    #looks good
                    user= User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
                    #login after register
                    # auth.login(request,user)
                    # message.success(request,"You are Logged in")
                    # return redirect('index')
                    user.save()
                    messages.success(request,"You are registered and can log in")
                    return redirect('login')



        else:
            messages.error(request,'Passwords do not match')
            return redirect('register')
    else:
        return render(request,"accounts/register.html")

def login(request):
    if request.method == 'POST':
        #login
        username=request.POST["username"]
        password=request.POST["password"]

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            print(123)
            auth.login(request,user)
            messages.success(request,"You are now Logged In")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request,"accounts/login.html")

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,"You are successfully LoggedOut")
        return redirect("index")

def dashboard(request):
    user_contacts= Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context={
        "contacts":user_contacts
    }

    return render(request,"accounts/dashboard.html",context)
