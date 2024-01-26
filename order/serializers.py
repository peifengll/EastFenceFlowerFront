#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from models.models import User, Order


class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'time', 'stage', 'address_id', 'money', 'user_id',
                  'remark', 'cart_id']
    # fields = '__all__'
    # exclude = ['keyword']
