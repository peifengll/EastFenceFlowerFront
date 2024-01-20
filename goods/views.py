from django.shortcuts import render
from rest_framework.views import APIView

from goods.serializers import GoodsInfoSerializer
from libs.utils.base_response import BaseResponse
from models.models import Goods


# Create your views here.

class GoodsInfo(APIView):
    def get(self, request):
        infos = Goods.objects.filter(size='0091')
        print(infos)
        ser = GoodsInfoSerializer(infos, many=True)
        return BaseResponse(data=ser.data, status=200)


class GoodsSort(APIView):
    def get(self, request):
        a = request.GET.get("id")
        infos = Goods.objects.filter(good_sort=a, size="0091")
        ser = GoodsInfoSerializer(infos, many=True)
        return BaseResponse(data=ser.data, status=200)


class GoodsDetail(APIView):
    def get(self, request):
        goodsid = request.GET.get("id")
        data = Goods.objects.select_related('flower').all()
        result = []
        for item in data:
            result.append({
                'flower_id': item.flower.flower_id,
                'charge': item.charge,
                'total_num': item.total_num,
                'salenum': item.salenum,
                'fname': item.flower.fname,
                'enname': item.flower.enname,
                'brithplace': item.flower.brithplace,
                'enplace': item.flower.enplace,
                'image': item.flower.image,
                'image2': item.flower.image2,
                'image3': item.flower.image3,
                'use': item.flower.use,
                'ldname': item.flower.ldname
            })
        # ser = GoodsInfoSerializer(, many=True)
        return BaseResponse(data=result, status=200)
