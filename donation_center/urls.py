from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dc),
    path('signup', views.signup, name="sign up"),
    path('logged_out', auth_views.LogoutView.as_view(), name="log out"),
    path('login', views.login),

    path('used', views.used_view),
    path('used_added', views.add_used),
    path('donated', views.donated_view),
    path('donated_added', views.add_donated),
    path('manage_requests', views.manage_requests_view),
    path('request_added', views.request_added),
    path('change_display_state', views.change_state),
    path('success', views.success, name='success'),
    path('send_broadcast_email', views.send_email_to_donor)
]