from django.shortcuts import render
import json
from pybo.models import Rate
from pybo.serializers import RateSerializer
from django.http import JsonResponse

def requestRate(request):
    if request.method == 'POST':
        try:
            InputData = json.loads(request.body)
            print(InputData)
            serializer_class = RateSerializer(data=InputData)
            if serializer_class.is_valid():
                if requestRateCheck(InputData["childnum"], InputData["talenum"]) == -1:
                    serializer_class.save()
                    average_rate = requestRatescore(InputData["talenum"])
                    return JsonResponse({"message": "success", "average_rate": str(average_rate)})
                else:
                    Rate.objects.filter(childnum=InputData["childnum"], talenum=InputData["talenum"]).update(rate=InputData["rate"])
                    average_rate = requestRatescore(InputData["talenum"])
                    return JsonResponse({"message": "success", "average_rate": str(average_rate)})
        except Exception as e:
            # 모든 예외 처리
            return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)
    else:
        return render(request, "pybo/index.html")

def requestRateList(num):
    try:
        queryset = Rate.objects.filter(talenum=num).order_by('-writedate')
        if queryset:
            list = [i for i in queryset.values()]
            return list
        else:
            return False
    except Exception as e:
        # 모든 예외 처리
        return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)

def requestRatescore(num):
    try:
        queryset = Rate.objects.filter(talenum=num)
        if queryset:
            rate = 0
            for i in queryset.values():
                rate += i["rate"]
            rate /= len(queryset)

            return round(rate, 2)
        else:
            return False
    except Exception as e:
        # 모든 예외 처리
        return JsonResponse({"message": "오류 발생: " + str(e)}, status=400)

def requestRateCheck(child, tale):
    try:
        rate = Rate.objects.get(childnum=child, talenum=tale)
        serializer_class = RateSerializer(rate, many=False)

        if rate:
            print(serializer_class.data["rate"])
            return serializer_class.data["rate"]

    except Rate.DoesNotExist:
        return -1
