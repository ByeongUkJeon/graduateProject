from django.shortcuts import render
import json
from pybo.models import Tale, Qna, Likes, Commentlikes

from pybo.serializers import LikesSerializer, CommentlikesSerializer
from django.http import JsonResponse

# Create your views here.


def requestLike(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            #childnum talenum
            print(InputData)
            if InputData["commentid"] == "": # 동화 자체 좋아요
                serializer_class = LikesSerializer(data=InputData)
                tale = Tale.objects.get(num=InputData["talenum"])

                if (not likeCheck(InputData["childnum"], InputData["talenum"], 'TALE')) and serializer_class.is_valid():
                    print('동화 좋아요 ADD')
                    serializer_class.save()
                    tale.likes += 1
                    tale.save()
                    return JsonResponse({"message": "success", "likeNum": tale.likes})
                elif likeCheck(InputData["childnum"], InputData["talenum"], 'TALE'):
                    try:
                        LIKE = Likes.objects.get(childnum=InputData["childnum"], talenum=InputData["talenum"])
                        LIKE.delete()
                        tale.likes -= 1
                        tale.save()
                        print("동화 좋아요 해제")
                        return JsonResponse({"message": "success", "likeNum": tale.likes})
                    except Likes.DoesNotExist:
                        print("좋아요 없음")
                        return JsonResponse({"message": "failure"})
                else:
                    print("머임ㅋ 없으")
                    return JsonResponse({"message": "failure"})
            else:
                serializer_class = CommentlikesSerializer(data=InputData)
                qna = Qna.objects.get(num=InputData["commentid"])
                if (not likeCheck(InputData["childnum"], InputData["commentid"], 'COMMENT')) and serializer_class.is_valid():
                    print('Comment 좋아요 됨')

                    serializer_class.save()
                    qna.likes += 1
                    qna.save()
                    return JsonResponse({"message": "success", "likeNum": qna.likes})
                elif likeCheck(InputData["childnum"], InputData["commentid"], 'COMMENT'):
                    try:
                        commentLike = Commentlikes.objects.get(childnum=InputData["childnum"], commentid=InputData["commentid"])
                        commentLike.delete()
                        qna.likes -= 1
                        qna.save()
                        print("Comment 좋아요 해제")
                        return JsonResponse({"message": "success", "likeNum": qna.likes})
                    except Commentlikes.DoesNotExist:
                        print("commentLike 없음")
                        return JsonResponse({"message": "failure"})

        except Exception as e:
                # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")


def likeCheck(child, num, type):
    if type == "TALE":
        try:
            Like = Likes.objects.get(childnum=child, talenum=num)
            if Like:
                return True
        except Likes.DoesNotExist:
            return False
    elif type == "COMMENT":

        try:
            commentlike = Commentlikes.objects.get(childnum=child, commentid=num)
            if commentlike:
                return True
        except Commentlikes.DoesNotExist:
            return False
