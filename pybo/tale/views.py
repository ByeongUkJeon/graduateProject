from functools import reduce

from django.shortcuts import render
import json
import os

import pybo.views
from pybo.like import views as like_view
from pybo.rate import views as rate_view
from pybo.favorite import views as favorite_view
from django.db.models import Count, Q

from pybo.models import User, Tale, RecentReads
from django.http import HttpResponse
from datetime import datetime

from pybo.serializers import UserSerializer, TaleSerializer, RecentReadSerializer

from django.http import JsonResponse
from itertools import combinations

from kss import split_sentences


def combi(arr, n):
    result = []
    if n > len(arr):
        return result

    if n == 1:
        for i in arr:
            result.append([i])

    elif n > 1:
        for i in range(len(arr) - n + 1):
            for j in combi(arr[i + 1:], n - 1):
                result.append([arr[i]] + j)

    return result

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
        if request.method == 'GET':
            queryset = Tale.objects.filter(num=request.GET["num"])
            if queryset:
                num = Tale.objects.get(num=request.GET["num"])
                serializer_class = TaleSerializer(num, many=False)
                splits = split_sentences(serializer_class.data["content"])
                #audios = ["http://localhost:8000/pybo/requestAudio/?num=" + InputData["num"] + "&speed=" + InputData["speed"] + "&seq=" + str(x + 1) for
                #          x in range(len(splits))]
                audio_files = ["pybo/audio/" + str(request.GET["num"]) + "/" + str(request.GET["num"]) + "_A_A_" + str(i+1) + ".mp3" for i in range(len(splits))]
                print(audio_files[0])
                for i in range(len(splits)):
                    print(splits[i])
                    #synthesize_text(splits[i], InputData["num"], 'A', 1.2, str(i + 1))
            context = {'tale_id': request.GET["num"], 'sentences': splits, 'audio_files': audio_files}
            return render(request, 'C:\\djangoproject\\mysite\\pybo\\templates\\tale\\tale.html', context)
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
                # for i in range(len(splits)):
                #     print(splits[i])
                #     type = ['A', 'B', 'C', 'D']
                #     speed = [0.6, 0.8, 1.0, 1.2, 1.4]
                #     for T in type:
                #         for S in speed:
                #             pybo.views.synthesize_text(splits[i], InputData["num"], T, S, str(i + 1))

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
                    for i in range(len(splits)):
                        print(splits[i])
                        type = ['A', 'B', 'C', 'D']
                        speed = [0.6, 0.8, 1.0, 1.2, 1.4]
                        for T in type:
                            for S in speed:
                                pybo.views.synthesize_text(splits[i], InputData["num"], T, S, str(i + 1))
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
            favorite = favorite_view.favoriteCheck(InputData["childnum"], InputData["talenum"])
            data = {"message":"success", "like" : check, "rate" : str(rate), "favorite": favorite}
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
            speed = 'E'

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

def requestRecommend(childnum):
    readList = pybo.views.requestRecentlyRead(childnum)
    if readList:
        #print(readList[0]["genre"])
        genre = str(readList[0]["genre"]).replace(" ", "")
        #print(genre)
        genreList = genre.split(',')
        #print(genreList)
        # genreCombi = combi(list(genreList), i)

        q_objects = [Q(genre__contains=word) for word in genreList]
        combined_query = Q()
        print(q_objects)
        for q_object in q_objects:
            combined_query &= q_object
        print(combined_query)
        tales = Tale.objects.filter(combined_query).distinct().values_list('num')
        print([i for i in tales])
        s = [i for i in tales.values()]
        return s
        # for i in range(len(list(genreList)), 0, -1):
        #     #genreCombi = combi(list(genreList), i)
        #     genreCombi = combinations(genreList, i)
        #     for genres in genreCombi:
        #         print(genres)
        #         q_objects = [Q(genre__contains=word) for word in genres]
        #         combined_query = Q()
        #         print(q_objects)
        #         for q_object in q_objects:
        #             combined_query &= q_object
        #         tales = Tale.objects.filter(combined_query)
        #         s = [i for i in tales.values()]

    else:
        return []