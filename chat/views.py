from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse
from likes.serializers import LikesInfoSerializer
from models.models import Likes


# Create your views here.


class ChatShowView(APIView):
    def get(self, request):
        userid = request.GET.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证缺失", status=401)
        try:
            res = queryAllChatById(userid=userid)
        except Exception as e:
            return BaseResponse(msg="查询失败", status=500)
        return BaseResponse(msg="操作成功", data=res, status=200)


def queryAllChatById(userid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                * 
            FROM
                chat 
            WHERE
                userId = %s;
          """, [userid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for i in result:
            tem = queryMsgByChatId(i["chatId"])
            i["msgGroup"] = tem
    return result


def queryMsgByChatId(chatid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                * 
            FROM
                msg 
            WHERE
                chatId = %s;
          """, [chatid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result
