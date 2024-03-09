import traceback

from django.shortcuts import render
import json
from rest_framework import viewsets


from pybo.models import User, Tale, Child, Ttssetting, Qna, Rate, Likes, Favorite, Commentlikes


from pybo.serializers import UserSerializer, TaleSerializer, ChildSerializer, TtsSettingSerializer, QnaSerializer, RateSerializer, LikesSerializer, FavoriteSerializer, CommentlikesSerializer

from django.http import JsonResponse

# Create your views here.

import os
def requestFavorite(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            serializer_class = FavoriteSerializer(data=InputData)
            #childnum talenum
            if (not favoriteCheck(InputData["childnum"], InputData["talenum"])) and serializer_class.is_valid():
                serializer_class.save()
                return JsonResponse({"message": "success"})
            elif favoriteCheck(InputData["childnum"], InputData["talenum"]):
                try:
                    favorite = Favorite.objects.get(childnum=InputData["childnum"], talenum=InputData["talenum"])
                    favorite.delete()
                    return JsonResponse({"message": "success"})
                except Favorite.DoesNotExist:
                    return JsonResponse({"message": "failure"})
            else:
                return JsonResponse({"message": "failure"})
        except Exception as e:
                # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")

def favoriteCheck(child, num):
    try:
        favorite = Favorite.objects.get(childnum=child, talenum=num)
        if favorite:
            return True

    except Favorite.DoesNotExist:
        return False



