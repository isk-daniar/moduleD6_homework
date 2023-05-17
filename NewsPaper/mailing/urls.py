from django.urls import path
from .views import MailingView

app_name = 'appointments'

urlpatterns = [
    path('make_mailing/', MailingView.as_view(), name="make_mailing"),
]