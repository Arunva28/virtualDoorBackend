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
            accounts_info = AccountsModel.objects.filter(expenseApproved=False)
            print(request.user)
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            email = request.user.email
            accounts_info = AccountsModel.objects.filter(Q(user=email) & Q(expenseApproved=False))
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def view(self, request):

        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        if is_admin is True:
            accounts_info = AccountsModel.objects.filter(expenseApproved=False)
            print(request.user)
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            email = request.user.email
            accounts_info = AccountsModel.objects.filter(Q(user=email) & Q(expenseApproved=False))
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = ""
        valid_user = ""
        accounts = ""
        serializer_user = ""
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        buildning_name = request.data['buildingName']
        houseNo = request.data['houseNo']
        unitNo = request.data['unitNo']
        filter_data = ""
        serializer_user = AddUserSerializer(filter_data, many=True)
        if is_admin is True:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['user']) &
                                                      Q(buildingName=buildning_name) &
                                                      Q(houseNo=houseNo) & Q(unitNo=unitNo))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data and buildning_name == user.buildingName and unitNo == user.unitNo :
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

                else:
                    return Response("user not found in the Building, House, or Unit Records", status=status.HTTP_401_UNAUTHORIZED)

        else:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['user']) &
                                                  Q(buildingName=buildning_name) &
                                                      Q(houseNo=houseNo) & Q(unitNo=unitNo))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data and request.data['user'] == user.user_id:
                    try:
                        accounts = Description.objects.get(Fields=request.data['Type'])
                    finally:
                        if accounts:
                            serializer = AccountsSerializer(data=request.data)
                            if request.data['Type'] == "Maintenance":
                                if serializer.is_valid(raise_exception=ValueError):
                                    serializer.save()
                                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                            else:
                                return Response("No privilege to add other payments expect MAINTENANCE",
                                                status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            return Response("Drop down selection invalid", status=status.HTTP_401_UNAUTHORIZED)

                return Response("Unauthorized, user not found in the Building, House, or Unit Records ",
                                status=status.HTTP_401_UNAUTHORIZED)

    def put(self,request):
        user = ""
        try:
            user = UserInfo.objects.get(user=request.user)
        finally:
            is_admin = user.isAdmin
            valid_user =""
            response = ""
            field_to_update = request.data['id']
            field = AccountsModel.objects.get(id=field_to_update)
            if is_admin is False and request.data['expenseApproved'] is True:
                return Response("Only admin can approve the amount", status=status.HTTP_401_UNAUTHORIZED)

        try:
            valid_user = UserInfo.objects.get(user_id=request.data['user'])
        except:
            valid_user = ""
        finally:
            if valid_user:
                if valid_user.buildingName == request.data['buildingName'] and valid_user.unitNo == request.data[
                    'unitNo'] and valid_user.houseNo == request.data['houseNo'] and field.user == request.data['user']:

                    if field.expenseApproved != request.data['expenseApproved'] and is_admin is True:
                        field.expenseApproved = request.data['expenseApproved']
                        response = response + "Expense Approved, "

                    if str(field.Amount) == str(request.data['Amount']):
                        print()
                    else:
                        field.Amount = request.data['Amount']
                        response = response + "Amount Updated, "

                    if field.IsExpense == request.data['IsExpense']:
                        print()
                    else:
                        field.IsExpense = request.data['IsExpense']
                        response = response + "Updated Income/Expense, "

                    if str(field.Date) != str(request.data['Date']):
                        field.Date = request.data['Date']
                        response = response + "Date updated "

                    if str(field.Type) != str(request.data['Type']) and is_admin is True:
                        field.Type = request.data['Type']

                    elif str(field.Type) != str(request.data['Type']) and is_admin is False:
                        return Response("Only admin can change the type of account",
                                        status=status.HTTP_401_UNAUTHORIZED)

                    field.save()
                    if response == "":
                        response = "No data Change"
                    return Response(response, status=status.HTTP_200_OK)


        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

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






