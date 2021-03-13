from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import DonorSignUpForm, LastDonDateForm
from .models import Donor, LastDonDate
from django.contrib.auth import login as auth_login


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/donor/')
            else:
                message = "Invalid username or password."
                return render(request, 'donor/login.html', {'form': form, 'message': message})
        else:
            message = "Invalid username or password."
            return render(request, 'donor/login.html', {'form': form, 'message': message})
    form = AuthenticationForm()
    return render(request, 'donor/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = DonorSignUpForm(request.POST)
        profile = Donor()
        if form.is_valid():
            try:
                profile.blood_group = form.cleaned_data.get('blood_group')
                profile.username = form.cleaned_data.get('username')
                profile.county = form.cleaned_data.get('county')
                profile.dob = form.cleaned_data.get('date_of_birth')
                profile.contact = form.cleaned_data.get('contact')
                profile.email = form.cleaned_data.get('email')
                profile.subscribe = form.cleaned_data.get('subscribe')
                profile.email = form.cleaned_data.get('email')

                user = form.save()
                user.refresh_from_db()
                user.save()
                profile.save()
                return redirect('/donor/login')

            except:
                message = "Date format should be 'YYYY-MM-DD'"
                return render(request, 'donor/signup.html', {'form': form, 'message': message})

    else:
        form = DonorSignUpForm()
    return render(request, 'donor/signup.html', {'form': form})


def home(request):
    user = request.user.username
    lastdondate = LastDonDateForm()
    sub = Donor.objects.filter(username=user)
    ldd = LastDonDate.objects.all().order_by('-date').filter(username=user)

    return render(request, 'donor/donor.html',
                  {'lastdondate': lastdondate, 'ldd': ldd, 'sub': sub})


def savedonationdate(request):
    ldd = LastDonDate()
    ldd.username = request.user.username
    ldd.venue = request.POST.get('venue')
    ldd.date = request.POST.get('date')
    ldd.save()

    user = request.user.username
    ldd = LastDonDate.objects.all().order_by('-date').filter(username=user)
    lastdondate = LastDonDateForm()
    message = "Last donation date is updated!"
    return render(request, 'donor/donor.html',
                  {'lastdondate': lastdondate, 'message': message, 'ldd': ldd})


@csrf_exempt
def savesubscriptionstate(request):
    username = request.user.username
    sub = Donor.objects.get(username=username)
    sub.subscribe = request.POST.get('status')
    sub.save()
    return redirect('/donor/')
