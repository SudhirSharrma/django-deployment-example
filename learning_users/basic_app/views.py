from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm, UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')



def register(request):
    registered=False
    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password) #here we are hashing the Password
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user # here are relating additional fields prefile information with original one to one relationship

            # check if profile pic was loaded
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form=UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                                {'user_form':user_form,
                                 'profile_form':profile_form,
                                 'registered':registered})

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        #use djamgo's built in authenticate Function
        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                #login
                login(request,user)
                #redirect user to index poge
                return HttpResponseRedirect(reverse('index'))
            else:
                #if user is not is_active
                return HttpResponse("Your Account is not active")
        else:
            print("User {} is invalid".format(username))
            return HttpResponse("Invalid Details Supplied")
            print("someone tried with incorrect login")

    else:
        return render(request, 'basic_app/login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return render(request, 'basic_app/special.html')
