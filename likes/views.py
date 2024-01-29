from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse
from likes.serializers import LikesInfoSerializer
from models.models import Likes


# Create your views here.

class LikesAddView(APIView):
    def post(self, request):
        userid = request.data.get("user_id")
        flowerid = request.data.get("flower_id")
        price = request.data.get("price")
        image = request.data.get("image")
        if userid is None or flowerid is None or userid == "" or flowerid == "":
            return BaseResponse(msg='flowerid 和 userid 不能为空', status=306)
        try:
            c = Likes.objects.filter(user_id=userid, flower_id=flowerid)
            if (c is not None) and len(c) > 0:
                print("flowerid and userod is exist", c)
                return BaseResponse(msg="已经添加过喜欢了", status=309)
            Likes.objects.create(
                user_id=userid,
                flower_id=flowerid,
                price=price,
                image=image,
            )
        except Exception as e:
            return BaseResponse(msg='服务器内部错误', status=500)
        return BaseResponse(msg='添加喜欢成功', status=200)


class LikesShowView(APIView):
    def get(self, request):
        userid = request.GET.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg='未获取到用户凭证', status=401)
        infos = []
        try:
            infos=custom_query(userid=userid)
        except Exception as e:
            return BaseResponse(msg='内部错误' + e.__str__(), status=500)
        return BaseResponse(msg='添加喜欢成功', data=infos, status=200)


class LikesDelView(APIView):
    def delete(self, request):
        print("**************")
        print("执行否")
        print("**************")
        print(request.data)
        likes_id = request.data.get("id")
        print("**************")
        print(likes_id)
        print("**************")
        if likes_id is None or likes_id == "":
            return BaseResponse(msg='未获取到对应id', status=307)
        try:
            Likes.objects.filter(
                flower_id=likes_id,
            ).delete()
        except Exception as e:
            return BaseResponse(msg='删除失败' + e.__str__(), status=500)
        return BaseResponse(msg='删除成功', status=200)



def custom_query(userid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
               l.flower_id,
               l.image,
               l.price,
               f.enname,
               f.fname
            FROM
                `likes` l
            INNER JOIN flower f ON l.flower_id = f.flower_id
            WHERE
                l.user_id = %s;
        """, [userid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result
