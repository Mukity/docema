from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from django.core.mail import send_mail
from django.db.models import Sum

from .models import BloodRequest, BloodUsed, BloodDonated, Events, Profile
from .forms import SignUpForm, EventForm
from donor.models import Donor
from docema import settings




@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile = Profile()
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_staff = True
            profile.donation_center = form.cleaned_data.get('donation_center')
            profile.email = form.cleaned_data.get('email')
            profile.location = form.cleaned_data.get('location')
            profile.contact = form.cleaned_data.get('contact')
            profile.county = form.cleaned_data.get('county')
            profile.username = form.cleaned_data.get('username')
            user.save()
            profile.save()
            return redirect('/donation_center/login')
    else:
        form = SignUpForm()
    return render(request, 'donation_center/sign_up.html', {'form': form})


def dc(request):
    user = request.user
    Bused = BloodUsed.objects.filter(dc_id=user).aggregate(Sum('units_used'))
    Bused = list(Bused.values())
    Bused = Bused[0]

    Brequest = BloodRequest.objects.filter(dc_id=user).filter(display="Yes").aggregate(Sum('units_required'))
    Trequest = BloodRequest.objects.filter(dc_id=user).aggregate(Sum('units_required'))
    Brequest = list(Brequest.values())
    Trequest = list(Trequest.values())
    Brequest = Brequest[0]
    Trequest = Trequest[0]

    Bdonated = BloodDonated.objects.filter(dc_id=user).aggregate(Sum('units_donated'))
    Bdonated = list(Bdonated.values())
    Bdonated = Bdonated[0]

    try:
        remaining = Bdonated-Bused
    except:
        remaining =0

    try:
        percentage_used = Bused/remaining*100
    except:
        percentage_used = 0

    form = EventForm()
    return render(request, 'donation_center/dc.html',
                  {'form': form, 'used': Bused, 'donated': Bdonated, 'Brequest': Brequest,
                   'Trequest': Trequest, 'remaining': remaining, 'percentage_used': percentage_used})


def success(request):
    form = EventForm(request.POST, request.FILES)
    event = Events()
    if form.is_valid():
        event.event_name = form.cleaned_data['event_name']
        event.poster = form.cleaned_data['poster']
        event.dc_id = request.user.username
        event.location = form.cleaned_data['location']
        event.date = form.cleaned_data['date']
        event.time = form.cleaned_data['time']
        event.save()
        message = "Event Uploaded"
    else:
        message = ("Ensure that: "
                   "Date format is YYYY-MM-DD. "
                   "Time  is in 24hr format e.g. 10:00 for a.m or 22:00 for p.m."
                   "or Event Name already exists")
    return render(request, 'donation_center/dc.html', {'form': form, 'message': message})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/donation_center/')
            else:
                message = "Invalid username or password."
                return render(request, 'donation_center/login.html', {'form': form, 'message': message})
        else:
            message = "Invalid username or password."
            return render(request, 'donation_center/login.html', {'form': form, 'message': message})
    form = AuthenticationForm()
    return render(request, 'donation_center/login.html', {'form': form})


def donated_view(request):
    donated = BloodDonated.objects.all().order_by('-date').filter(dc_id=request.user.username)
    return render(request, 'donation_center/donated.html', { "donated":donated })


@csrf_exempt
def add_donated(request):
    donate = BloodDonated()
    donate.donation_id = request.POST.get('donatedID')
    donate.units_donated = request.POST.get('units')
    donate.blood_group = request.POST.get('donatedGroup')
    donate.dc_id = request.user.username
    donate.date = request.POST.get('donatedDate')
    donate.save()
    message = "Blood donated entry has been added"
    donated = BloodDonated.objects.all().order_by('-date').filter(dc_id=request.user.username)
    return render(request, 'donation_center/donated.html', {"message": message, "donated": donated})


def manage_requests_view(request):
    requests = BloodRequest.objects.all().order_by('-date').filter(dc_id=request.user.username)
    return render(request, 'donation_center/manage_requests.html', {"requests": requests})


@csrf_exempt
def request_added(request):
    add_request = BloodRequest()
    add_request.blood_group = request.POST.get('requestBGroup')
    add_request.display = request.POST.get('display')
    add_request.dc_id = request.user.username
    add_request.request_id = request.POST.get('requestID')
    add_request.units_required = request.POST.get('requestUnits')
    add_request.save()
    message = "Request Added!"
    requests = BloodRequest.objects.all().order_by('-date').filter(dc_id=request.user.username)
    return render(request, 'donation_center/manage_requests.html', {"message": message, "requests": requests})


@csrf_exempt
def change_state(request):
    if BloodRequest.objects.filter(request_id=request.POST.get('requestID')).exists():
        state = BloodRequest.objects.get(request_id=request.POST.get('requestID'))
        state.display = request.POST.get('display')
        state.save()
        message = "State Changed!"
    else:
        message = "Request not available in database!"
    requests = BloodRequest.objects.all().order_by('-date')
    return render(request, 'donation_center/manage_requests.html', {"message": message, "requests": requests})


def used_view(request):
    used = BloodUsed.objects.all().order_by('-date').filter(dc_id=request.user.username)
    return render(request, 'donation_center/used.html', { "used": used })


@csrf_exempt
def add_used(request):
    use = BloodUsed()
    use.date = request.POST.get('usedDate')
    use.dc_id = request.user.username
    use.used_id = request.POST.get('usedID')
    use.blood_group = request.POST.get('usedBGroup')
    use.units_used = request.POST.get('usedUnits')
    use.save()
    message = "Blood used entry has been made"
    used = BloodUsed.objects.all().order_by('-date').filter(dc_id=request.user.username)
    return render(request, 'donation_center/used.html', {"message": message, "used": used})


def send_email_to_donor(request):
    donors = Donor.objects.filter(subscribe=True)

    user =request.user.username
    dc_name = Profile.objects.filter(username=user)

    for name in dc_name:
        dc = name.donation_center
        contact = name.contact
        location = name.location
        county = name.county

    recipient_list = []
    for donor in donors:
        email = donor.email
        recipient_list.append(email)

    form = EventForm(request.POST, request.FILES)
    subject = "Urgent Blood Donor Needed"
    message = "Hello Donor,\n\n Hope this mail finds you well. We would like to request for you to donate blood or " \
              "share the message with people you may know in you area. The donation facility is " + dc +\
              " located at " + location + " in " + county + " county.\n You can contact them on the number " + contact + \
              ". \n\nThank you for your response to help save a life."
    email_from = settings.EMAIL_HOST_USER

    send_mail(subject, message, email_from, recipient_list)
    message = "E-mail has been send to subscribed Donors"
    return render(request, 'donation_center/dc.html', {'form': form, 'message': message})