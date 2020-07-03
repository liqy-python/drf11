from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from day10.models import User


class MyAuth(BaseAuthentication):
    # 重写authenticate
    def authenticate(self, request):
        # 获取认证信息
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        print(auth)
        if auth is None:
            return None

        # 设置认证信息的校验规则
        auth_list = auth.split()

        # 校验规则：是否是合法用户  是不是两段式  如果第一个不是auth就错误
        if not (len(auth_list) == 2 and auth_list[0].lower() == "auth"):
            raise exceptions.AuthenticationFailed("认证信息有误，认证失败")

        if auth_list[1] != "admin123":
            raise exceptions.AuthenticationFailed("用户信息校验失败")

        # 最后校验数据库是否存在此用户
        user = User.objects.filter(username="admin123").first()

        if not user:
            raise exceptions.AuthenticationFailed("用户不存在")
        return (user, None)