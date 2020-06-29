from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import settings
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from day06app.models import User
"""
Django视图模式两种：
FBV: 函数视图  function base view  基于函数定义的逻辑视图
CBV: 类视图    class base view     基于类定义的视图
"""


# @csrf_protect  # 全局禁用csrf的情况 为某个视图单独添加csrf认证
@csrf_exempt  # 为某个视图免除csrf认证
def user(request):
    if request.method == "GET":
        print("GET SUCCESS  查询")
        # TODO 查询用户的相关逻辑
        return HttpResponse("GET SUCCESS")

    elif request.method == "POST":
        print("POST SUCCESS  添加")
        # TODO 添加用户的相关的逻辑
        return HttpResponse("POST SUCCESS")

    elif request.method == "PUT":
        print("PUT SUCCESS  修改")
        return HttpResponse("PUT SUCCESS")

    elif request.method == "DELETE":
        print("DELETE SUCCESS  删除")
        return HttpResponse("DELETE SUCCESS")


"""
单条：获取单条  获取所有  添加单个  删除单个  整体更新单个  局部更新单个
群体：增加多个  删除多个  整体修改多个   局部修改多个
"""


@method_decorator(csrf_exempt, name="dispatch")  # 让类视图免除csrf认证
class UserView(View):
    """
    类视图内部通过请求的方法来匹配到对应的内部的函数，从而进行对应的处理
    """

    def get(self, request, *args, **kwargs):
        """
        提供查询单个用户与多个用户的操作
        :param request:  用户id
        :return: 查询后的用户信息
        """

        # 获取用户的id
        user_id = kwargs.get("id")
        if user_id:  # 查询单个
            user_val = User.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_val:
                # 如果查询出对应的用户信息，则将用户的信息返回到前端
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_val
                })
        else:
            # 如果没有传参数id  代表查询所有
            user_list = User.objects.all().values("username", "password", "gender")
            # print(type(user_list))
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })

        return JsonResponse({
            "status": 500,
            "message": "查询失败",
        })

    def post(self, request, *args, **kwargs):
        """
        新增单个用户
        """
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                "status": 201,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        print(user_id,username,pwd)
        try:
            if user_id:
                user_obj=User.objects.get(pk=user_id)
                print(user_obj)
                user_obj.name = username
                user_obj.password = pwd
                user_obj.save()
                return JsonResponse({
                    "status": 203,
                    "message": "修改用户名成功",
                    "results": {"username": user_obj.username, "password": user_obj.password}
                })
        except:
            return JsonResponse({
                "status": 500,
                "message": "修改用户数据失败",
            })

    def delete(self, request, *args, **kwargs):
        # request:  WSGIrequest
        user_id = kwargs.get("id")
        try:
            username = User.objects.filter(pk=user_id).values("username").first()
            User.objects.get(pk=user_id).delete()
            return JsonResponse({
                "status": 203,
                "message": "删除用户成功",
                "results": {"username": username}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "删除用户失败",
            })


# 开发基于drf的视图
class UserAPIView(APIView):
    # 单独为某个视图指定渲染器  局部使用
    # 局部的要比全局的优先级高
    renderer_classes = (BrowsableAPIRenderer,)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user_val = User.objects.get(pk=user_id)
        # request：<rest_framework.request.Request>
        # get(self, request, *args, **kwargs):  DRF视图中的request事 经过封装后的request对象  其中包含原生的request
        # 可以通过_request 访问Django原生的request对象
        # print(request._request.GET)
        # 通过DRF 的request对象获取参数
        # print(request.GET)
        # 通过query_params来获取参数
        print(request.query_params)

        # 获取路径传参
        user_id = kwargs.get("pk")

        return Response("DRF GET SUCCESS")

    def post(self, request, *args, **kwargs):
        # post请求传递参数的形式  form-data  www-urlencoded  json
        print(request._request.POST)  # Django 原生的request对象
        print(request.POST)  # DRF 封装后的request对象
        # 可以获取多种格式的参数 DRF 扩展的请回去参数  兼容性最强
        print(request.data)

        return Response("POST GET SUCCESS")


class StudentAPIView(APIView):
    # 局部使用解析器
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print("POST方法")

        # print(request.POST)
        print(request.data)

        return Response("POST方法访问成功")