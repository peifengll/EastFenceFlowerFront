#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from models.models import Cart


class CartShowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        # exclude = ['keyword']
