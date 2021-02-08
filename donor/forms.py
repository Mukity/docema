from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from donor.models import LastDonDate, Donor

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

Blood_group = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('0+', '0+'), ('0-', '0-'),
]
boolean_choices = [
    (True, 'Yes'), (False, 'No')
]


class DonorSignUpForm(UserCreationForm):
    contact = forms.CharField(max_length=15, required=True, help_text='Phone number Required')
    county = forms.CharField(max_length=20, required=True, help_text='County name Required',
                             widget=forms.Select(choices=Counties))
    date_of_birth = forms.CharField(required=True)
    blood_group = forms.CharField(max_length=3, widget=forms.Select(choices=Blood_group))
    subscribe = forms.BooleanField(widget=forms.Select(choices=boolean_choices))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'contact',
                  'blood_group', 'email', 'county', 'password1', 'subscribe')


class LastDonDateForm(forms.ModelForm):
    class Meta:
        model = LastDonDate
        fields = ['venue', 'date']