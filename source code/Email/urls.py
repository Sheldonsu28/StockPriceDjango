from django.urls import path

from . import views

urlpatterns = [
    path('send_mail/<str:symbol>', views.send_email_to_user, name='send mail to user'),
]
