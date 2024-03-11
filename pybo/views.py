import traceback

from django.shortcuts import render
import json
from rest_framework import viewsets

from pybo.like.views import likeCheck
from pybo.models import User, Tale, Child, Ttssetting, Qna, Rate, Likes, Favorite, Commentlikes, RecentReads

from django.core import serializers

from .rate import views as rate_views
from pybo.serializers import TaleSerializer, ChildSerializer, TtsSettingSerializer, CommentlikesSerializer, RecentReadSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from google.cloud import texttospeech
# Create your views here.

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Downloads\\sacred-reality-380304-de688212e474.json"



def synthesize_text(text, num, type, speed, count="main"):
    """Synthesizes speech from the input string of text."""

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=str(text))

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-WaveNet-" + type,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=-1.0,
        speaking_rate=speed

    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    if speed == 1.0:
        speed = 'A'
    elif speed == 1.2:
        speed = 'B'
    elif speed == 1.4:
        speed = 'C'
    elif speed == 0.8:
        speed = 'D'
    elif speed == 0.6:
        speed = 'E'
    # The response's audio_content is binary.
    with open("pybo/audio/" + str(num) + "/" + str(num) + '_' + type + "_" + speed + "_" + count + ".mp3", "wb") as out:
        out.write(response.audio_content)
        print(str(num) + count + ".mp3")

def downloadImage(request):
    try:
        tales = Tale.objects.values()

        for i in range (50, len(tales)):
            link = tales[i]['imglink']
            os.system("curl " + link + " > " + str(i + 1) + ".jpg")
        return HttpResponse("헉")
    except:
        return JsonResponse({"message": "연결 오류"}, status=400)

def requestHome(request):
    try:

        if request.method == 'POST':
            InputData = json.loads(request.body)

            queryset = Child.objects.filter(num=InputData["childId"])
            print("뭔데")
            favorites = []
            if queryset:
                TTSSETTING = Ttssetting.objects.get(childnum=InputData['childId'])
                setting_object = TtsSettingSerializer(TTSSETTING, many=False)
                favorite = Favorite.objects.filter(childnum=InputData['childId'])
                readList = requestRecentlyRead(InputData['childId'])
                if favorite:
                    favoriteNums = [i["talenum_id"] for i in favorite.values()]
                    for i in favoriteNums:
                        taleSet = Tale.objects.get(num=i)
                        serializer_class = TaleSerializer(taleSet, many=False)
                        average_rate = rate_views.requestRatescore(i)
                        serializer_class.data["rate"] = average_rate
                        favorites.append(serializer_class.data)
                else:
                    favorites = []

                data = {
                    "state": "success",
                    "ttsSetting": setting_object.data,
                    "favorites": favorites,
                    "recently" : readList
                }

                return JsonResponse(data)
            else:
                print("에러 발생")
                return JsonResponse({"message": "faliure"})

    except Exception as e:

# 모든 예외 처리

        return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)


def requestSearch(request):
    try:
        if request.method == 'POST':
            InputData = json.loads(request.body)

            type = InputData['type']
            search = str(InputData['search'])
            print(search)
            if type == "title":
                taleSet = Tale.objects.all().filter(title__contains=search)

                tales = [tale for tale in taleSet.values()]
                for t in tales:
                    average_rate = rate_views.requestRatescore(t["num"])
                    t["rate"] = average_rate
                result = {"count": len(taleSet), "searchResult": tales}
                return JsonResponse(result)


    except:

        return JsonResponse({"message": "연결 오류"}, status=400)



def requestRecentlyRead(childnum):
    try:
        recentread = RecentReads.objects.filter(childnum = childnum).order_by('-readdate')

        if recentread:
            readList = [i for i in recentread.values()]
            return readList
        else:
            return False

    except:

        return JsonResponse({"message": "연결 오류"}, status=400)




