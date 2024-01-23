#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from cart.views import CartAddView
from cart.views import CartShow

urlpatterns = [
    path('add', CartAddView.as_view()),
    path('show', CartShow.as_view()),
]

