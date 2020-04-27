from django.shortcuts import render
from basicapp.forms import UserProfileInfoForm,UserForm
# Create your views here.

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def index(request):

    return render(request,'basicapp/index.html')

@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))




def register(request):

    #checking if the user is registered or not
    registered = False

    if request.method == "POST":
        #grabbing the info off the forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        #checking if all the forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            #if the forms are valid, we grab info from the user form
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #grabbing info from the profile form
            profile = profile_form.save(commit = False)

            #this line reperesents the one to one relationship bw the user and profile form
            profile.user = user

            #double checking if there is a picture in there before savinf
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print (user_form.errors,profile_form.errors)

    else:
        #if the request is not POST then creating the instances of user form and profile form
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basicapp/registration.html',
        {'user_form':user_form,'profile_form':profile_form,'registered':registered})




def user_login(request):

    if request.method == "POST":
        username = request.POST.get('usename')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else :
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print ("someone tried to login and failed")
            print ("usename : {} and password".format(username,password))
            return HttpResponse("invalid login details")


    else:
        return render(request,'basicapp/login.html',{})
