from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from utils.response import APIResponse


class SendMessageRate(SimpleRateThrottle):
    scope = "send"

    # 只对含有手机号的请求做验证
    def get_cache_key(self, request, view):
        phone = request.query_params.get("phone")
        if not phone:
            return None
        # 根据手机号动态展示返回的值
        return 'throttle_%(scope)s_%(ident)s' % {"scope": self.scope, "ident": phone}


