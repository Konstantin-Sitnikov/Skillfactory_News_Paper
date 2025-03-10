from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from sign.models import BaseRegisterForm

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/protect/login/'