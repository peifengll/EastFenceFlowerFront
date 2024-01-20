from django.shortcuts import render
from rest_framework.views import APIView

from flowerInfo.serializers import FlowerInfoSerializer
from libs.utils.base_response import BaseResponse
from models.models import Flower


# Create your views here.

class FlowerInfos(APIView):
    def get(self, request):
        infos = Flower.objects.filter()
        print("------------------")
        print(infos)
        ser = FlowerInfoSerializer(infos, many=True)
        print("------------------")
        return BaseResponse(data=ser.data, status=200)
