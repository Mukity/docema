from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from donation_center.models import Events

Counties = [
    ('Mombasa', 'Mombasa'), ('Kwale', 'Kwale'), ('Kilifi', 'Kilifi'), ('Tana River', 'Tana River'),
    ('Lamu', 'Lamu'), ('Taita/Taveta', 'Taita/Taveta'), ('Garissa', 'Garissa'), ('Wajir', 'Wajir'),
    ('Mandera', 'Mandera'), ('Marsabit', 'Marsabit'), ('Isiolo', 'Isiolo'), ('Meru', 'Meru'),
    ('Tharaka-Nithi', 'Tharaka-Nithi'), ('Embu', 'Embu'), ('Kitui', 'Kitui'), ('Machakos', 'Machakos'),
    ('Makueni', 'Makueni'), ('Nyandarua', 'Nyandarua'), ('Nyeri', 'Nyeri'), ('Kirinyaga', 'Kirinyaga'),
    ("Murang'a", "Murang'a"), ('Kiambu', 'Kiambu'), ('Turkana', 'Turkana'), ('West Pokot', 'West Pokot'),
    ('Samburu', 'Samburu'), ('Trans Nzoia', 'Trans Nzoia'), ('Uasin Gishu', 'Uasin Gishu'),
    ('Elgeyo/Marakwet', 'Elgeyo/Marakwet'), ('Nandi', 'Nandi'), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'),
    ('Nakuru', 'Nakuru'), ('Narok', 'Narok'), ('Kajiado', 'Kajiado'), ('Kericho', 'Kericho'), ('Bomet', 'Bomet'),
    ('Kakamega', 'Kakamega'), ('Vihiga', 'Vihiga'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'),
    ('Siaya', 'Siaya'), ('Kisumu', 'Kisumu'), ('Homa Bay', 'Homa Bay'), ('Migori', 'Migori'),
    ('Kisii', 'Kisii'), ('Nyamira', 'Nyamira'), ('Nairobi City', 'Nairobi City')
]


class SignUpForm(UserCreationForm):
    donation_center = forms.CharField(max_length=50, required=True, help_text='Required')
    email = forms.EmailField(max_length=100, required=True, help_text='E-mail Required')
    contact = forms.CharField(max_length=15, required=True, help_text='Phone number Required')
    county = forms.CharField(max_length=20, required=True, help_text='County name Required',
                             widget=forms.Select(choices=Counties))
    location = forms.CharField(max_length=254, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'donation_center', 'contact', 'email', 'county', 'location', 'password1')


class EventForm(forms.ModelForm):
    poster = forms.ImageField(label='Select Poster Image')

    class Meta:
        model = Events
        fields = ['event_name', 'location', 'date', 'time', 'poster']
