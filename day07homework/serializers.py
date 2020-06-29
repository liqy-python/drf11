from rest_framework import serializers

# 定义序列化器类 跟模型moles对应的
from day07homework.models import Stu
from pycharm_drf import settings


# 序列化器
class StuSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # 自定义字段 返回盐  使用SerializerMethodField来定义
    salt = serializers.SerializerMethodField()
    def get_salt(self, obj):
        return "salt"

    # 自定义性别的返回值
    gender = serializers.SerializerMethodField()

    # self 是当前序列化器  obj是对象
    def get_gender(self, obj):
        # print(obj.gender, type(obj))
        # 性别是choices类型  get_字段名_display()直接访问值
        return obj.get_gender_display()


# 反序列化器
class StuDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=8,
        min_length=4,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    password = serializers.CharField(required=False)
    # 继承的serializer类并没有新增做具体的实现

    def create(self, validated_data):
        # 方法中完成新增
        print(validated_data)
        return Stu.objects.create(**validated_data)
