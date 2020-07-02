from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from day07api.models import Employee
from .serializers import EmployeeSerializer, EmployeeDeSerializer


class EmployeeAPIView(APIView):

    def get(self, request, *args, **kwargs):

        user_id = kwargs.get("pk")

        if user_id:
            # 查询单个
            emp_obj = Employee.objects.get(pk=user_id)
            # 查询出的单个的员工对象无法直接序列化，需要使用序列化器完成序列化
            # .data 将序列化器的数据打包成字典
            emp_ser = EmployeeSerializer(emp_obj)
            data = emp_ser.data

            return Response({
                "status": 200,
                "msg": "查询单个员工成功",
                "results": data,
            })
        else:

            # 查询所有
            # 员工对象无法直接序列化返回到前台
            emp_list = Employee.objects.all()

            # TODO  使用序列化器完成多个员工的序列化  需要指定many=True
            emp_list_ser = EmployeeSerializer(emp_list, many=True).data

            return Response({
                "status": 200,
                "msg": "查询所有员工成功",
                "results": emp_list_ser,
            })

    def post(self, request, *args, **kwargs):
        """
        新增单个对象
        """
        user_data = request.data

        # TODO 前端发送的数据需要入库时  必须对前台的数据进行校验
        if not isinstance(user_data, dict) or user_data == {}:
            return Response({
                "status": 501,
                "msg": "数据有误",
            })

        # 使用序列化器对前台提交的数据进行反序列化
        # 在反序列化时需要指定关键字参数  data
        serializer = EmployeeDeSerializer(data=user_data)
        # print(serializer)
        print(serializer.is_valid())
        # 对序列化的数据进行校验  通过is_valid() 方法对传递过来的参数进行校验  校验合法返回True
        print(serializer.is_valid())
        if serializer.is_valid():
            # 调用save()去保存对象  必须重写create()方法
            # create() 方法保存成功后会返回 员工实例
            emp_obj = serializer.save()
            # 将创建成功的用户实例返回到前端
            return Response({
                "status": 201,
                "msg": "用户创建成功",
                "results": EmployeeSerializer(emp_obj).data
            })
        else:
            return Response({
                "status": 501,
                "msg": "用户创建失败",
                # 验证失败后错误信息包含在 .errors中
                "results": serializer.errors
            })