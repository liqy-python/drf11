from rest_framework.permissions import BasePermission
from day10.models import User


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        # 只读 所有人都可以访问
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        username = request.data.get("username")
        # 写操作  判断用户是否有登录信息
        user = User.objects.filter(username=username).first()
        print(user)
        if user:
            return True
        return False
