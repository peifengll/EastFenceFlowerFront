#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from chat.views import ChatShowView

urlpatterns = [
    path('show', ChatShowView.as_view()),
]
