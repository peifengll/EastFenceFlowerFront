#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from user.views import LoginView, RegisterView, UploadView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('upload', UploadView.as_view(),name='upload_handle'),
]
