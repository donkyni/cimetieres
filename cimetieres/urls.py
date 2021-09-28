
from django.conf.urls import url

from cimetieres import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard')
]