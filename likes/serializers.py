#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from models.models import Likes


class LikesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        # fields = '__all__'
        exclude = ['user_id']
