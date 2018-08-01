from django.shortcuts import render
from .models import AccountsModel, Description
from .serializers import AccountsSerializer, AccountsDescriptionSerializer, AccountsExpenseSerializer
from userinfo.serializers import AddUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userinfo.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q
from datetime import datetime


# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@method_decorator(csrf_exempt, name='post')
class AccountsView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):
        #if user.is
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        if is_admin is True:
            accounts_info = AccountsModel.objects.all()
            print(request.user)
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            email = request.user.email
            print(email)
            accounts_info = AccountsModel.objects.filter(user=email)
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = ""
        valid_user = ""
        accounts = ""
        serializer_user = ""
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        filter_data = ""
        serializer_user = AddUserSerializer(filter_data, many=True)
        if is_admin is True:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['user']) &
                                                  Q(buildingName=request.data['buildingName']))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data:
                    try:
                        accounts = Description.objects.get(Fields=request.data['Type'])
                    finally:
                        if accounts:
                            if False:
                                try:
                                    date = request.data['Date']
                                except:
                                    date = datetime.now()
                                    date = date.date()
                                    date = str(date)
                                    request.data['Date'] = date
                                Comparison_Date = date.split('-')
                                Integer_ComaprisonDate = []
                                Date_Now = []

                                Date_from_API = datetime.now()
                                Date_from_API = Date_from_API.date()
                                Date_from_API = str(Date_from_API)
                                Date_from_API = Date_from_API.split('-')
                                for i in range(0, len(Comparison_Date)):
                                    b = int(Comparison_Date[i])
                                    c = int(Date_from_API[i])
                                    Date_Now.append(c)
                                    Integer_ComaprisonDate.append(b)
                                for i in range(0, 1):
                                    if Integer_ComaprisonDate[0] > Date_Now[0]:
                                        break
                                    else:
                                        if Integer_ComaprisonDate[0] == Date_Now[0]:
                                            if Integer_ComaprisonDate[1] > Date_Now[1]:
                                                break
                                            else:
                                                if Integer_ComaprisonDate[1] == Date_Now[1]:
                                                    if Integer_ComaprisonDate[2] >= Date_Now[2]:
                                                        break
                                                    else:
                                                        return Response("invalid date",
                                                                        status=status.HTTP_401_UNAUTHORIZED)
                                                else:
                                                    return Response("invalid date", status=status.HTTP_401_UNAUTHORIZED)
                                        else:
                                            return Response("invalid date", status=status.HTTP_401_UNAUTHORIZED)
                            serializer = AccountsSerializer(data=request.data)
                            if serializer.is_valid(raise_exception=ValueError):
                                serializer.save()
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response("Drop down selection invalid", status=status.HTTP_401_UNAUTHORIZED)

                else:
                    return Response("User doesnt exist in the building specified", status=status.HTTP_401_UNAUTHORIZED)

        else:
            try:
                accounts = Description.objects.get(Fields=request.data['Type'])
            finally:
                if accounts:
                    serializer = AccountsSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=ValueError):
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("Drop down selection invalid", status=status.HTTP_401_UNAUTHORIZED)

            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        field_to_delete = request.data['id']
       # print(AccountsModel.objects)
        field = AccountsModel.objects.get(id=field_to_delete)
        if is_admin is True:
            try:
                field.delete()
                return Response("Entry Deleted Successfully", status=status.HTTP_200_OK)
            except AccountsSerializer.DoesNotExist:
                return Response("Entry Not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='get')
class AccountsDropdownview(APIView):

    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):

        Dropdown = Description.objects.all()
        serializer = AccountsDescriptionSerializer(Dropdown, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin

        if is_admin is True:
            Description(Fields=request.data['Fields']).save()
            return Response(request.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        field_to_delete = request.data['Fields']
        field = Description.objects.get(Fields=field_to_delete)
        if is_admin is True:
            try:
                field.delete()
                return Response("Field Deleted Successfully", status=status.HTTP_200_OK)
            except Description.DoesNotExist:
                return Response("Field Not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class Expenses(APIView):

    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def post(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        serializer_user=""
        filter_data= ""
        Data_int = 0
        Send_data = []
        serializer_user = AddUserSerializer(filter_data, many=True)
        if is_admin is False:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['UserId']) &
                                                  Q(buildingName=request.data['buildingName']))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data:
                    filter_data=  AccountsModel.objects.filter(Q(Date__year= request.data['Year']) &
                                                       Q(Date__month= request.data['Month']) &
                                                               Q(user=request.data['UserId']) &
                                                               Q(IsExpense= False))

                    Serializer_data = AccountsExpenseSerializer(filter_data, many=True)
                    Data_int = 0
                    for eachelement in Serializer_data.data:
                        Data = str(eachelement)
                        Data = Data.split(',')
                        Data= Data[1].split(')')
                        Data_1 = list(Data[0])
                        Data_1 = Data_1[2:-1]
                        Data_1 = ''.join(Data_1)
                        Data_int = Data_int + float(Data_1)
                    Send_data.append(Data_int)
                    filter_data=  AccountsModel.objects.filter(Q(Date__year= request.data['Year']) &
                                                       Q(Date__month= request.data['Month']) &
                                                               Q(user=request.data['UserId']) &
                                                               Q(IsExpense= True))

                    Serializer_data = AccountsExpenseSerializer(filter_data, many=True)
                    Data_int = 0
                    for eachelement in Serializer_data.data:
                        Data = str(eachelement)
                        Data = Data.split(',')
                        Data= Data[1].split(')')
                        Data_1 = list(Data[0])
                        Data_1 = Data_1[2:-1]
                        Data_1 = ''.join(Data_1)
                        Data_int = Data_int + float(Data_1)
                    Send_data.append(Data_int)

                    return Response(Send_data, status=status.HTTP_200_OK)

            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)






