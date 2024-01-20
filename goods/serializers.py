#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from models.models import Goods


class GoodsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'