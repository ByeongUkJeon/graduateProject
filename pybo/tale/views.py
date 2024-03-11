
from django.shortcuts import render
import json
import os

import pybo.views
from pybo.like import views as like_view
from pybo.rate import views as rate_view
from pybo.models import User, Tale, RecentReads
from django.http import HttpResponse
from datetime import datetime

from pybo.serializers import UserSerializer, TaleSerializer, RecentReadSerializer

from django.http import JsonResponse

from kss import split_sentences

def addTale(request):


    if request.method == 'POST':
        # try:
            InputData = json.loads(request.body)

            serializer_class = TaleSerializer(data=InputData)
            if serializer_class.is_valid():
                serializer_class.save()
                return JsonResponse({"message": "UPLOAD_SUCCESS"})
            else:
                return JsonResponse({"message": "FAILURE"})

    else:
        return render(request, "pybo/index.html")


def requestTTS(request):
    try:

        if request.method == 'POST':
            InputData = json.loads(request.body)

            queryset = Tale.objects.filter(num=InputData["num"])
            f = "pybo/audio/" + str(InputData["num"]) + "/" + str(InputData["num"]) + "_A_1_1" + ".mp3"
            # 우분투 f = "/home/jeon/venv/test/pybo/audio/" + str(InputData["num"]) + "/" + str(InputData["num"]) + "_A_1_1" + ".mp3"
            print(f)
            if queryset:
                num = Tale.objects.get(num=InputData["num"])
                serializer_class = TaleSerializer(num, many=False)
                splits = split_sentences(serializer_class.data["content"])
                #audios = ["http://localhost:8000/pybo/requestAudio/?num=" + InputData["num"] + "&speed=" + InputData["speed"] + "&seq=" + str(x + 1) for
                #          x in range(len(splits))]
                for i in range(len(splits)):
                    print(splits[i])
                    #synthesize_text(splits[i], InputData["num"], 'A', 1.2, str(i + 1))
                if os.path.isfile(f) or os.path.isdir("pybo/audio/" + str(InputData["num"])):
                    data = {
                        "state" : "success",
                        "imglink": "http://localhost:8000/pybo/requestImage/?num=" + InputData["num"],
                        "title": serializer_class.data['title'],
                        #"content" : serializer_class.data['content'],
                       # "tts_audio" : audios,
                        "tts_text" : splits
                    }
                    return JsonResponse(data)
                else:
                    print("엘스")

                    os.mkdir("pybo/audio/" + str(InputData["num"]))

                    #synthesize_text("안녕하세요~~~", InputData["num"])
                    # synthesize_text(serializer_class.data["content"], num)
                    data = {
                        "state" : "success",
                        "imglink": "http://112.152.27.80:8000/pybo/requestImage/?num=" + InputData["num"],
                        "title": serializer_class.data['title'],
                        #"content" : serializer_class.data['content'],
                     #   "tts_audio" : audios,
                        "tts_text": splits

                    }
                    return JsonResponse(data)


            else:
                print("동화 존재 X")
                return JsonResponse({"message": "faliure"})


    except KeyError:
        return JsonResponse({"message": "연결 오류"}, status=400)

    else:
        return render(request, "pybo/index.html")


def requestTale(request):
    try:

        if request.method == 'POST':
            InputData = json.loads(request.body)

            queryset = Tale.objects.filter(num=InputData["num"])

            if queryset:
                num = Tale.objects.get(num=InputData["num"])
                serializer_class = TaleSerializer(num, many=False)
                splits = split_sentences(serializer_class.data["content"])
                average_rate = rate_view.requestRatescore(InputData["num"])
                saveRecentlyRead(InputData)
                #for i in range(len(splits)):
                    #print(splits[i])
                    #synthesize_text(splits[i], InputData["num"], 'A', 1.2, str(i + 1))
                data = {
                    "state" : "success",
                    "imglink": "http://localhost:8000/pybo/requestImage/?num=" + InputData["num"],
                    "title": serializer_class.data['title'],
                    "tts_text" : splits,
                    "likes" : serializer_class.data["likes"],
                    "reviews" : serializer_class.data["reviews"],
                    "views" : serializer_class.data["views"],
                    "rate" : average_rate
                }
                print(data)
                num.views += 1
                num.save()
                # data["rates"] = requestRateList(InputData["num"])
                # data["like"] = likeCheck(InputData["childnum"], InputData["num"])
                # data["favorite"] = favoriteCheck(InputData["account"], InputData["num"])
                return JsonResponse(data)


            else:
                print("동화 존재 X")
                return JsonResponse({"message": "faliure"})

    except Exception as e:
        return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)

    else:
        return render(request, "pybo/index.html")

def requestCheck(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            check = like_view.likeCheck(InputData["childnum"], InputData["talenum"], "TALE")
            rate = rate_view.requestRateCheck(InputData["childnum"], InputData["talenum"])
            data = {"message":"success", "like" : check, "rate" : str(rate)}
            return JsonResponse(data)
        except Exception as e:
            # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")



def requestImage(request):
    try:
        num = request.GET['num']
        file = "pybo/images/" + str(num) + ".jpg"
        with open(file, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpg")
    except:
        return JsonResponse({"message": "연결 오류"}, status=400)

def saveRecentlyRead(InputData):
    print(InputData)
    current_time = datetime.now()
    recentRead = RecentReadSerializer(data={"childnum": InputData["childnum"], "talenum": InputData["num"]})

    if recentRead.is_valid():
        try:
            RR = RecentReads.objects.get(childnum=InputData["childnum"], talenum=InputData["num"])
            print("레전드레전드")
            if RR:
                RR.readdate = current_time
                RR.save()
                print("여기임?1")
                return True

        except RecentReads.DoesNotExist:
            recentRead.save()
            print("여기임?2")
            return True
        except Exception as e:
            # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)

def requestAudio(request):
    try:
        num = request.GET['num']
        seq = request.GET['seq']
        speed = request.GET['speed']
        type = request.GET['type']
        queryset = Tale.objects.filter(num=num)
        if speed == '1.0':
            speed = 'A'
        elif speed == '1.2':
            speed = 'B'
        elif speed == '1.4':
            speed = 'C'
        elif speed == '0.8':
            speed = 'D'
        elif speed == '0.6':
            speed = 'F'

        f = "pybo/audio/" + str(num) + "/" + str(num) + '_' + type + '_' + speed + '_' + str(seq) + ".mp3"
        print(f)
        if queryset:
            num = Tale.objects.get(num=num)
            serializer_class = TaleSerializer(num, many=False)

            if os.path.isfile(f):
                print(f)
                audio = open(f, "rb")
                response = HttpResponse()
                response.write(audio.read())
                response['Content-Type'] = 'audio/mp3'
                response['Content-Length'] = os.path.getsize(f)

                return response
    except:
        return JsonResponse({"message": "연결 오류"}, status=400)