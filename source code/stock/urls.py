from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_home_page', views.user_home_page, name='user_home_page'),
    path('subscribe_stocks', views.subscribe_stocks, name='subscribe_stocks'),
    path('unsubscribe_stocks/<str:symbol>', views.delete_subscription, name='delete_subscription'),
    path('register', views.register_user, name='register_user')
]
