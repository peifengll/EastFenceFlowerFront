#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from models.models import Flower


class FlowerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = '__all__'


class FlowerGoodsSerializer(serializers.Serializer):
    flower_id = serializers.IntegerField()
    charge = serializers.FloatField()
    total_num = serializers.IntegerField()
    salenum = serializers.IntegerField()
    fname = serializers.CharField()
    enname = serializers.CharField()
    brithplace = serializers.CharField()
    enplace = serializers.CharField()
    image = serializers.CharField()
    image2 = serializers.CharField()
    image3 = serializers.CharField()
    use = serializers.CharField()
    ldname = serializers.CharField()

class FlowerGoodsDetailSerializer(serializers.Serializer):
    flower_id = serializers.IntegerField()
    charge = serializers.FloatField()
    total_num = serializers.IntegerField()
    salenum = serializers.IntegerField()
    fname = serializers.CharField()
    enname = serializers.CharField()
    brithplace = serializers.CharField()
    enplace = serializers.CharField()
    image = serializers.CharField()
    image2 = serializers.CharField()
    image3 = serializers.CharField()
    use = serializers.CharField()
    ldname = serializers.CharField()
