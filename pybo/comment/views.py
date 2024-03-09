import traceback

from django.shortcuts import render
import json
from pybo.models import User, Tale, Child, Ttssetting, Qna, Rate, Likes, Favorite, Commentlikes
from pybo.serializers import UserSerializer, TaleSerializer, ChildSerializer, TtsSettingSerializer, QnaSerializer, RateSerializer, LikesSerializer, FavoriteSerializer, CommentlikesSerializer
from django.http import JsonResponse

# Create your views here.

import os

def requestComment(request):
    try:
        if request.method == 'POST':
            InputData = json.loads(request.body)
            print(InputData)
            InputData["likes"] = 0
            serializer_class = QnaSerializer(data=InputData)
            if serializer_class.is_valid():
                serializer_class.save()
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "failure"})



    except:

        return JsonResponse({"message": "연결 오류"}, status=400)


def requestCommentList(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            queryset = Qna.objects.filter(talenum=InputData["talenum"]).order_by('-writedate')
            commentLikeCheck = Commentlikes.objects.filter(childnum=InputData["childnum"])
            likelist = [i["commentid_id"] for i in commentLikeCheck.values()]
            if queryset:
                RDATA = {"message": "success", "list": [i for i in queryset.values()]}
                for i in RDATA["list"]:
                    i["nickname"] = User.objects.get(account=i["parent_id"]).nickname
                    child = Child.objects.get(num=i["childnum_id"])
                    print(child)
                    i["type"] = child.type
                    i["childAge"] = child.age
                    i["personality"] = child.personality

                RDATA["likeList"] = likelist
                return JsonResponse(RDATA)

            else:
                print("QNA 없으")
                return JsonResponse({"message": "success", "list": []})
        except Exception as e:
            # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")