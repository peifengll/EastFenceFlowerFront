#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from order.views import OrderAddView, OrderListView, OrderUpdateView, OrderShowView

urlpatterns = [
    path('add', OrderAddView.as_view()),
    path('allinfo', OrderListView.as_view()),
    path('update', OrderUpdateView.as_view()),
    path('show', OrderShowView.as_view()),
]

