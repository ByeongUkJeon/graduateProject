import traceback

from django.shortcuts import render
import json
from rest_framework import viewsets
from pybo.models import User, Tale, Child, Ttssetting, Qna, Rate, Likes, Favorite

from django.core import serializers

from pybo.serializers import UserSerializer, TaleSerializer, ChildSerializer, TtsSettingSerializer, QnaSerializer, RateSerializer, LikesSerializer, FavoriteSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from google.cloud import texttospeech
from kss import split_sentences
from django.db.models import Count
# Create your views here.

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Downloads\\sacred-reality-380304-de688212e474.json"



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
                    "views" : serializer_class.data["views"]
                }
                num.views += 1
                num.save()
                data["rates"] = requestRateList(InputData["num"])
                data["like"] = likeCheck(InputData["childnum"], InputData["num"])
                data["favorite"] = favoriteCheck(InputData["account"], InputData["num"])
                return JsonResponse(data)


            else:
                print("동화 존재 X")
                return JsonResponse({"message": "faliure"})

    except Exception as e:
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

            if queryset:
                TTSSETTING = Ttssetting.objects.get(childnum=InputData['childId'])
                setting_object = TtsSettingSerializer(TTSSETTING, many=False)

                data = {
                    "state" : "success",
                    "ttsSetting" : setting_object.data,

                }
                return JsonResponse(data)
            else:
                print("에러 발생")
                return JsonResponse({"message": "faliure"})


    except KeyError:
        return JsonResponse({"message": "연결 오류"}, status=400)

    else:
        return render(request, "pybo/index.html")

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
                result = {"count": len(taleSet), "searchResult": tales}
                return JsonResponse(result)


    except:

        return JsonResponse({"message": "연결 오류"}, status=400)

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

            if queryset:

                RDATA = {"message" :  "success"}
                RDATA["list"] = [i for i in queryset.values()]
                return JsonResponse(RDATA)

            else:
                print("QNA 없으")
                return JsonResponse({"message": "failure"})
        except KeyError:
            return JsonResponse({"message": "연결 오류"}, status=400)
    else:
        return render(request, "pybo/index.html")

def requestLike(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            serializer_class = LikesSerializer(data=InputData)
            #childnum talenum
            if InputData["request"] == "LIKE" and serializer_class.is_valid():

                serializer_class.save()
                return JsonResponse({"message": "success"})
            elif InputData["request"] == "CANCEL":

                try:
                    LIKE = Likes.objects.get(childnum=InputData["childnum"], talenum=InputData["talenum"])
                    LIKE.delete()
                    return JsonResponse({"message": "success"})
                except Likes.DoesNotExist:
                    return JsonResponse({"message": "failure"})

            else:
                print("QNA 없으")
                return JsonResponse({"message": "failure"})
        except Exception as e:
                # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")

def requestRate(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            serializer_class = RateSerializer(data=InputData)
            #childnum talenum
            if InputData["request"] == "add" and serializer_class.is_valid():
                serializer_class.save()
                return JsonResponse({"message": "success"})
            elif InputData["request"] == "delete":
                try:
                    RATE = Rate.objects.get(parent=InputData["parent"], talenum=InputData["talenum"])
                    RATE.delete()
                    return JsonResponse({"message": "success"})
                except RATE.DoesNotExist:
                    return JsonResponse({"message": "failure"})

            else:
                return JsonResponse({"message": "failure"})
        except Exception as e:
                # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")

def requestRateList(num):
    try:
        queryset = Rate.objects.filter(talenum=num).order_by('-writedate')
        print(queryset)
        if queryset:
            list = [i for i in queryset.values()]
            print(list)
            return list
        else:
            return False
    except Exception as e:
        # 모든 예외 처리
        return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)


def requestFavorite(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            serializer_class = FavoriteSerializer(data=InputData)
            #childnum talenum
            if InputData["request"] == "add" and serializer_class.is_valid():
                serializer_class.save()
                return JsonResponse({"message": "success"})
            elif InputData["request"] == "delete":
                try:
                    favorite = Favorite.objects.get(parent=InputData["parent"], talenum=InputData["talenum"])
                    favorite.delete()
                    return JsonResponse({"message": "success"})
                except favorite.DoesNotExist:
                    return JsonResponse({"message": "failure"})
            else:
                return JsonResponse({"message": "failure"})
        except Exception as e:
                # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")

def favoriteCheck(parent, num):
    try:
        favorite = Favorite.objects.get(parent=parent, talenum=num)
        if favorite:
            return True

    except Favorite.DoesNotExist:
        return False


def likeCheck(child, num):
    try:
        Like = Likes.objects.get(childnum=child, talenum=num)

        if Like:
            return True

    except Likes.DoesNotExist:
        return False

