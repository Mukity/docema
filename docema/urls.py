from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.home_view),

    path('donation_center/', include('donation_center.urls')),
    path('donor/', include('donor.urls')),

    path('requests', views.blood_requests),
    path('events', views.blood_events),

    path('feedback_submitted', views.feedback_submitted),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
