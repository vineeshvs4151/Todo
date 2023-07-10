from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import *
from api.serializer import *
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

# Create your views here.


'''Create view with using APIView'''

# class TodoView(APIView):

#     def get(self,request,*Args,**kw):
#         qs=TodosModel.objects.all()
#         serializer=Todoserializer(qs,many=True)
#         return Response(data=serializer.data)




'''
Create view using Viewset.
While using ViewSet their is no standard http request like(get,post,pu/patch,delete).
Here http methods are (list,create,retrieve,update,destroy)
'''


# class TodoView(ViewSet):

#     def list(Self,request,*Args,**kw):
#         qs=TodosModel.objects.all()
#         serializer=Todoserializer(qs,many=True)
#         return Response(data=serializer.data)
    
#     def create(self,request,*Args,**kw):
#         serializer=Todoserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
        
    
#     def retrieve(self,request,*Args,**kw):
#         id=kw.get("pk")
#         qs=TodosModel.objects.get(id=id)
#         serializer=Todoserializer(qs,many=False)
#         return Response(data=serializer.data)
    
#     def destroy(self,request,*Args,**kw):
#         id=kw.get("pk")
#         TodosModel.objects.get(id=id).delete()
#         return Response(data="Deleted Successfully")
    
#     def update(self,request,*Args,**kw):
#         id=kw.get("pk")
#         obj=TodosModel.objects.get(id=id)
#         serializer= Todoserializer(data=request.data,instance=obj)
#         if(serializer.is_valid()):
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)



'''Create view using with ModelViewSet'''

class TodoView(ModelViewSet):
    
    authentication_classess=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Todoserializer
    queryset=TodosModel.objects.all() 


    # def list(self,request,*Args,**kw):
    #     loggedUser=request.user
    #     qs=TodosModel.objects.filter(user=loggedUser)
    #     serializer=Todoserializer(qs,many=True)
    #     return Response(data=serializer.data)

    def get_queryset(self):
        return TodosModel.objects.filter(user=self.request.user)
    

    def create(self,request,*Args,**kw):
        serializer=Todoserializer(data=request.data)
        if serializer.is_valid():
            TodosModel.objects.create(**serializer.validated_data,user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    



#   Creating a custom method .
#   While creating a custom methos we have to use the action decorator for defining which method is this.
    @action(methods=["GET"],detail=False)
    def pending_todo(self,request,*Args,**kw):
        qs=TodosModel.objects.filter(status=False)
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
    


    @action(methods=["GET"],detail=False)
    def completed_todo(self,request,*Args,**kw):
        qs=TodosModel.objects.filter(status=True)
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
    


    @action(methods=["GET"],detail=True)
    def mark_as_done(self,request,*Args,**kw):
        id=kw.get("pk")
        qs=TodosModel.objects.filter(id=id)
        qs.update(status=True)
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
    

class UserView(ModelViewSet):

    serializer_class=RegisterSerializer
    queryset=User.objects.all() 

    """
    Here we override the default created method because here password 
    is not get hashed.So we use (create_user) method for hashing the password.
    """

    # def create(self,request,*Args,**kw):
    #     serializer=RegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    