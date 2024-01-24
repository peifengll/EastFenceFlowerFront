#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from models.models import Flower, Address


class AddressInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = '__all__'
        exclude = ['u_id']



