#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from models.models import Flower


class FlowerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = '__all__'