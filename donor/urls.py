from django.urls import path

from donor import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('', views.home),
    path('savedonationdate', views.savedonationdate),
    path('updatesubscription', views.savesubscriptionstate),
]