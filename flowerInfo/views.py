from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView

from flowerInfo.serializers import FlowerInfoSerializer, FlowerGoodsSerializer, FlowerGoodsDetailSerializer
from libs.utils.base_response import BaseResponse
from models.models import Flower


# Create your views here.

class FlowerInfos(APIView):
    def get(self, request):
        infos = Flower.objects.filter()
        ser = FlowerInfoSerializer(infos, many=True)
        return BaseResponse(data=ser.data, status=200)


class FlowerSort(APIView):
    def get(self, request):
        sort = request.GET.get("id")
        infos = custom_query1(sort_id=sort)
        ser = FlowerGoodsSerializer(infos, many=True)
        return BaseResponse(data=ser.data, status=200)


class FlowerAsGoods(APIView):
    def get(self, request):
        id = request.GET.get("id")
        infos = custom_query2(flower_id=id)
        # print(infos[0])
        ser = FlowerGoodsDetailSerializer(infos, many=True)

        return BaseResponse(data=ser.data, status=200)


# 连表查询
def custom_query1(sort_id=None):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                flower.flower_id, charge, total_num, salenum,
                fname, enname, brithplace, enplace, flower.image, image2, image3, `use`, ldname
            FROM flower, goods
            WHERE
                flower.flower_id = goods.flower_id
            and flower.sort= %s and goods.size="0091"
        """, [sort_id])

        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result


def custom_query2(flower_id=None):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                flower.flower_id, charge, total_num, salenum,nickname,`size`,intor,
                fname, enname, brithplace, enplace, flower.image, image2, image3, `use`, ldname
            FROM flower, goods
            WHERE
                flower.flower_id = %s
                and
                flower.flower_id = goods.flower_id
              
        """, [flower_id])

        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result
