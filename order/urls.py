#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from order.views import OrderAddView, OrderListView

urlpatterns = [
    path('add', OrderAddView.as_view()),
    path('allinfo', OrderListView.as_view()),
]

