import traceback

from django.shortcuts import render
import json
from rest_framework import viewsets
from pybo.models import User, Tale, Child, Ttssetting, Qna, Rate, Likes, Favorite, Commentlikes

from django.core import serializers

from pybo.serializers import UserSerializer, TaleSerializer, ChildSerializer, TtsSettingSerializer, QnaSerializer, RateSerializer, LikesSerializer, FavoriteSerializer, CommentlikesSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from google.cloud import texttospeech
from kss import split_sentences
from django.db.models import Count

def idCheck(request):

    if request.method == 'POST':
        InputData = json.loads(request.body)
        try:
            ID_DUPLICATE = User.objects.filter(account=InputData['account'])
            if ID_DUPLICATE:
                print("중복 있따")
                return JsonResponse({"message": "ID_DUPLICATE"})
            else:
                print("아이디 중복 없음!")
                return JsonResponse({"message": "ID_AVAILABLE"})
        except:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")

def nicknameCheck(request):

    if request.method == 'POST':
        InputData = json.loads(request.body)
        try:
            NICKNAME_DUPLICATE = User.objects.filter(account=InputData['nickname'])
            if NICKNAME_DUPLICATE:
                print("닉네임 중복")
                return JsonResponse({"message": "NICKNAME_DUPLICATE"})
            else:
                print("닉네임 중복 없음!")
                return JsonResponse({"message": "NICKNAME_AVAILABLE"})
        except:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")


def signup(request):

    if request.method == 'POST':
        try:

            InputData = json.loads(request.body)

            print(InputData)
            serializer_class = UserSerializer(data=InputData)
            if serializer_class.is_valid():
                serializer_class.save()
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "failure"})



        except KeyError:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")

def addChild(request):
    if request.method == 'POST':
        try:

            InputData = json.loads(request.body)

            print(InputData)
            serializer_class = ChildSerializer(data=InputData)
            if serializer_class.is_valid():
                childResult = serializer_class.save()
                ttsSerializer =  TtsSettingSerializer(data={"ttsspeed": "1.0", "ttsvoice" :"A","childnum" : childResult.num})
                print(ttsSerializer)
                if ttsSerializer.is_valid():
                    ttsSerializer.save()
                    return JsonResponse({"message": "success"})
                else:
                    return JsonResponse({"message": "failure"})
            else:
                return JsonResponse({"message": "failure"})



        except KeyError:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")



def login(request):

    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            queryset = User.objects.filter(Q(account=InputData['account']) and Q(passwd=InputData['passwd']))

            if queryset:
                ACCOUNT = User.objects.get(account=InputData['account'])
                serializer_class = UserSerializer(ACCOUNT,many=False)
                childCount = Child.objects.filter(parent=ACCOUNT).count()
                RDATA = {
                    'member_info': serializer_class.data,
                    'member_setting': {"setting_1": "3", "setting_2": "1.0"},
                    'message': "success"
                }
                if childCount > 0:
                    childset = Child.objects.filter(Q(parent=InputData['account']))
                    childs = [i for i in childset.values()]
                    RDATA['child'] = childs
                    print(RDATA)
                    return JsonResponse(RDATA)
                else:
                    RDATA['child'] = '0'
                    return JsonResponse(RDATA)
            else:
                print("로그인 X")
                return JsonResponse({"message": "로그인 실패"})
        except KeyError:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")


def requestChildProfile(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            queryset = User.objects.filter(Q(account=InputData['userId']))

            if queryset:
                ACCOUNT = User.objects.get(account=InputData['userId'])
                childCount = Child.objects.filter(parent=ACCOUNT).count()

                if childCount > 0:
                    childset = Child.objects.filter(Q(parent=InputData['userId']))
                    childs = [i for i in childset.values()]

                    RDATA = {
                        'message': "success"
                    }
                    RDATA['childProfileList'] = childs
                    print(RDATA)
                    return JsonResponse(RDATA)
                else:
                    RDATA = {
                        'message': "success"
                    }
                    RDATA['childProfileList'] = []
                    return JsonResponse(RDATA)
            else:
                print("로그인 X")
                return JsonResponse({"message": "로그인 실패"})
        except KeyError:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")