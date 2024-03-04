from django.http import HttpResponseForbidden


class AllowIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ip = '127.0.0.1'  # 여러 개의 IP 주소를 사용하려면 리스트로 저장 가능

        # 클라이언트의 IP 주소 확인
        client_ip = self.get_client_ip(request)

        # 허용된 IP 주소인지 확인
        if client_ip not in allowed_ip:
            return HttpResponseForbidden("접근이 거부되었습니다.")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print(ip)
        return ip