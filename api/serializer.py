from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User



class Todoserializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    status=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    class Meta:
        model= TodosModel
        fields= ["id","task_name","user","status","created_date"]
 


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields=["first_name","last_name","email","username","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)