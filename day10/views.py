from django.shortcuts import render
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import settings
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication

from day10.authentication import MyAuth
from day10.permissions import MyPermission
from day10.throttle import SendMessageRate
from day10.models import User
from utils.response import APIResponse
from django.contrib.auth.models import Group,Permission


class TestAPIView(APIView):
    # 局部配置
    authentication_classes = [MyAuth]

    def get(self, request, *args, **kwargs):
        # 查询创建的自定义用户
        user = User.objects.first()
        '''
        # 获取对应角色    管理员
        print(user.groups.first())
        # 获取对应权限
        print(user.user_permissions.first())

        # 获取角色
        group = Group.objects.first()
        print(group)
        # 获取对应权限
        print(group.permissions.first().name)
        # 获取对应的用户
        print(group.user_set.first().username)
        
        permission = Permission.objects.filter(pk=9).first()
        print(permission.name)
        # print(permission.user_set.first().username)   # 错误
        per = Permission.objects.filter(pk=13).first()
        print(per.name)
        # print(per.group_set.first().name)
        '''
        return APIResponse("OK")


class TestPermission(APIView):
    # 局部配置
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return APIResponse("登陆成功")


class UserLogin(APIView):
    scope = "login"
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [MyPermission]
    throttle_classes = [UserRateThrottle]

    def get(self,request,*args,**kwargs):
        return APIResponse("读操作")

    def post(self,request,*args,**kwargs):
        return APIResponse("写操作")


class SendMessageAPIView(APIView):
    throttle_classes = [SendMessageRate]

    def get(self, request, *args, **kwargs):
        return APIResponse("读操作访问成功")

    def post(self, request, *args, **kwargs):
        return APIResponse("写操作访问成功")