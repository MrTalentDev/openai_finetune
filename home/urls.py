from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import answer, setting

app_name = 'home'

urlpatterns = [
    path('', answer, name='home'),
    path('answer', answer, name='answer'),
    path('setting',  setting, name='setting'),
]