from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from datetime import datetime, date
from django.shortcuts import render
from django.db.models import Sum

from docema import settings
from donation_center.models import BloodRequest, BloodUsed, BloodDonated, Profile, Events


def home_view(request):
    year = datetime.today().year
    requests = BloodRequest.objects.filter(date__year=year).aggregate(Sum('units_required'))
    requests = list(requests.values())[0]
    donations = BloodDonated.objects.filter(date__year=year).aggregate(Sum('units_donated'))
    donations = list(donations.values())[0]
    used = BloodUsed.objects.filter(date__year=year).aggregate(Sum('units_used'))
    used = list(used.values())[0]
    return render(request, 'home.html', {'requests': requests, 'donations': donations, 'used': used, 'year': year})


@csrf_protect
def feedback_submitted(request):
    fullname = request.POST.get('fullName')
    email = request.POST.get('email')
    comment = request.POST.get('comment')

    subject = "DOCEMA FEEDBACK"
    message = comment + "\n\nFROM: " + str(fullname) + "\nEMAIL: " + str(email)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['brema2019.20@gmail.com']

    send_mail(subject, message, email_from, recipient_list)
    message = "Thank you for the feedback!!!"
    return render(request, 'home.html', {"message": message})


def blood_requests(request):
    br = BloodRequest.objects.filter(display="Yes").order_by('date')
    dc = Profile.objects.all
    return render(request, 'requests.html', {"blood_requests": br, "dc": dc})


def blood_events(request):
    dates = date.today()
    be = Events.objects.filter(date__gte=dates)
    return render(request, 'events.html', {"events": be})
