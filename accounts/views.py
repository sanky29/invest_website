from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User
from django.contrib.auth import authenticate,logout,login
from .forms import *
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from invest import settings
from django.contrib import messages
from .decorators import *


def home(request):
    return render(request, 'accounts/index.html')


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'accounts/register.html'


def verify_email(request):
    if request.method == 'GET':
        email = request.GET['email']
        user = User.objects.filter(email=email)
        print(email)
        if user.exists():
            return JsonResponse({"status":"1"})
        else:
            otp = random.randint(1000000, 9999999)
            request.session['attempts'] = 0
            request.session['otp'] = otp
            request.session['email'] = email
            sub = "One Time Password"
            message = "Hello " + request.GET['first_name'] + "\n" + "Your OTP is " + str(otp)
            print(otp)
            send_mail(sub, message, settings.EMAIL_HOST_USER, [email])
            return JsonResponse({"status":"0"})


def Submit(request):
    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp']:
            user=UserSignUpForm(request.POST)
            user.email = request.session['email']
            u = user.save()
            profile = Profile(user = u)
            profile.save()
            return JsonResponse({"status": "-1"})
        else:
            if request.session['attempts'] == 2:
                return JsonResponse({"status": "-2"})
            else:
                request.session['attempts'] += 1
                return JsonResponse({"status": str(request.session['attempts'])})
    if request.method == 'GET':
        if request.session['attempts'] == 2:
            return JsonResponse({"status": "-2"})
        else:
            request.session['attempts'] += 1
            sub = "Nykinsky One Time Password"
            message = "Hello " + request.GET['first_name'] + "\n" + "Your OTP is " + str(request.session['otp'])
            send_mail(sub, message, settings.EMAIL_HOST_USER, [request.session['email']])
            return JsonResponse({"status": str(request.session['attempts'])})


@unauthenticated_user
def signinview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'Email-id or Password Incorrect')
    return render(request, 'accounts/login.html')


@authenticated_user
def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        return render(request, 'accounts/logout.html')


@authenticated_user
def generalview(request):
    profile = Profile.objects.get(user = request.user.pk)
    context = {'User_name': request.user.first_name,
               'image':profile.image,
               'User_name2': request.user.last_name,
               'phone': request.user.phone,
               'email': request.user.email}
    return render(request, 'accounts/general.html', context)


@authenticated_user
def page(request):
    context = {'User_name': request.user.first_name}
    return render(request, 'accounts/mainpage.html', context)
