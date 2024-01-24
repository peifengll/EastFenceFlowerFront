#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from address.views import AddressShowView, AddressAddView, AddressDelView, AddressUpdateView

urlpatterns = [
    path('add', AddressAddView.as_view()),
    path('update', AddressUpdateView.as_view()),
    path('delete', AddressDelView.as_view()),
    path('allinfo', AddressShowView.as_view()),
]
