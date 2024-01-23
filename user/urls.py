#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from user.views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
]
