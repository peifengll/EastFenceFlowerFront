#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from order.views import OrderAddView

urlpatterns = [
    path('add', OrderAddView.as_view()),
]

