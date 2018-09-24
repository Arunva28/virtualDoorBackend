from django.shortcuts import render
from .models import AccountsModel, Description
from .serializers import AccountsSerializer, AccountsDescriptionSerializer, AccountsExpenseSerializer, AccountsExportSerializer
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
import xlsxwriter
from django.core.mail import EmailMessage
from io import StringIO, BytesIO


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
        print("mine1")
        is_admin = user.isAdmin
        if is_admin is True:
            accounts_info = AccountsModel.objects.filter(expenseApproved=False)
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
        buildning_name = user.buildingName#request.data['buildingName']
        #houseNo = #request.data['houseNo']
        unitNo = user.unitNo#request.data['unitNo']
        filter_data = ""
        serializer_user = AddUserSerializer(filter_data, many=True)
        if is_admin is True:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['user']) &
                                                      Q(buildingName=buildning_name) & Q(unitNo=unitNo))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data and buildning_name == user.buildingName and unitNo == user.unitNo :
                    try:
                        accounts = Description.objects.get(Fields=request.data['Type'])
                    finally:
                        if accounts:

                            request.data['houseNo'] = serializer_user.data[0]['houseNo']
                            request.data['unitNo'] = serializer_user.data[0]['unitNo']
                            request.data['buildingName'] = serializer_user.data[0]['buildingName']
                            serializer = AccountsSerializer(data=request.data)
                            if serializer.is_valid(raise_exception=ValueError):
                                serializer.save()
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response("Drop down selection invalid", status=status.HTTP_401_UNAUTHORIZED)

                elif request.data['user'] == "all":
                    data_user =""
                    iterations = 0
                    try:
                        filter_data = UserInfo.objects.filter(Q(buildingName=buildning_name) & Q(unitNo=unitNo))
                        serializer_user = AddUserSerializer(filter_data, many=True)

                    finally:
                        if serializer_user.data:
                            for eachelement in serializer_user.data:
                                iterations += 1
                            amount = float(request.data['Amount']) / float(iterations)
                            for eachelement in serializer_user.data:
                                try:
                                    accounts = Description.objects.get(Fields=request.data['Type'])
                                finally:
                                    if accounts:
                                        request.data['Amount'] = round(amount,2)
                                        request.data['user'] = eachelement['user']['email']
                                        request.data['houseNo'] = eachelement['houseNo']
                                        serializer = AccountsSerializer(data=request.data)
                                        if serializer.is_valid(raise_exception=ValueError):
                                            serializer.save()
                                            data_user = data_user + str(serializer.data)
                                    else:
                                        return Response("Drop down selection invalid", status=status.HTTP_401_UNAUTHORIZED)
                            return Response(data_user, status=status.HTTP_201_CREATED)
                        else:
                            return Response("Building or unit no incorrect", status=status.HTTP_401_UNAUTHORIZED)

                else:
                    return Response("user not found in the Building, House, or Unit Records", status=status.HTTP_401_UNAUTHORIZED)

        else:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['user']) &
                                                  Q(buildingName=buildning_name) & Q(unitNo=unitNo))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data and request.data['user'] == user.user_id:
                    try:
                        accounts = Description.objects.get(Fields=request.data['Type'])
                    finally:
                        if accounts:
                            serializer = AccountsSerializer(data=request.data)
                            if request.data['Type'] == "Maintenance":
                                request.data['houseNo'] = serializer_user.data[0]['houseNo']
                                request.data['unitNo'] = serializer_user.data[0]['unitNo']
                                request.data['buildingName'] = serializer_user.data[0]['buildingName']
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

                if  field.user == request.data['user']:

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
                        return Response(response, status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(response, status=status.HTTP_201_CREATED)


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
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        ite = 0
        serializer = AccountsDescriptionSerializer(Dropdown, many=True)
        if is_admin is True:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            for each in serializer.data:
                ite +=1
                if str(each['Fields']) == "Maintenance":
                    print(ite)
                    return Response(serializer.data[ite-1], status=status.HTTP_200_OK)


    def post(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin

        if is_admin is True:
            Description(Fields=request.data['Fields']).save()
            return Response(request.data, status=status.HTTP_201_CREATED)

        return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)

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
        nodata_indicate = 0.0
        serializer_user=""
        total_income = ""
        total_expense = ""
        filter_data= ""
        Data_int = 0.0
        Send_data = []
        data_dict_income_total ={}
        data_dict_expense_total = {}
        data_dict_income ={}
        income_s_dict ={}
        data_dict_expense ={}
        data_total ={}
        iterator =0
        list_dict = []
        serializer_user = AddUserSerializer(filter_data, many=True)
        if True:
            try:
                filter_data = UserInfo.objects.filter(Q(user_id=request.data['UserId']) &
                                                  Q(buildingName=request.data['buildingName']))
                serializer_user = AddUserSerializer(filter_data, many=True)
            finally:
                if serializer_user.data:
                    try:
                        filter_data=  AccountsModel.objects.filter(Q(Date__year= request.data['Year']) &
                                                       Q(Date__month= request.data['Month']) &
                                                               Q(user=request.data['UserId']) &
                                                                   Q(expenseApproved=True) &
                                                               Q(IsExpense= False))

                    finally:
                        if filter_data:
                            Serializer_data = AccountsExpenseSerializer(filter_data, many=True)
                            Data_int = 0.0

                            for eachelement in Serializer_data.data:
                                Data = eachelement['Amount']
                                Data_int = Data_int + float(Data)
                                data_dict_income_total['Total Income'] =  round(Data_int,2)
                        else:
                            data_dict_income_total['Total Income'] = round(Data_int,2)
                            nodata_indicate += 1

                        list_dict.append(data_dict_income_total)
                    try:
                        filter_data = AccountsModel.objects.filter(Q(Date__year=request.data['Year']) &
                                                                           Q(Date__month=request.data['Month']) &
                                                                           Q(user=request.data['UserId']) &
                                                                   Q(expenseApproved=True) &
                                                                           Q(IsExpense=True))
                    finally:
                        if filter_data:
                            Serializer_data = AccountsExpenseSerializer(filter_data, many=True)
                            Data_int = 0.0
                            for eachelement in Serializer_data.data:
                                Data = eachelement['Amount']
                                Data_int = Data_int + float(Data)
                                data_dict_expense_total['Total Expense'] = round(Data_int,2)
                        else:
                            data_dict_expense_total['Total Expense'] = round(Data_int,2)
                            nodata_indicate +=1

                        list_dict.append(data_dict_expense_total)
                        Dropdown = Description.objects.all()
                        serializer = AccountsDescriptionSerializer(Dropdown, many=True)
                        ite=0
                        for eachelement in serializer.data:
                            ite = ite + 1
                            data_expense = 0.0
                            data_income = 0.0
                            if data_dict_income.get(eachelement['Fields']) is None:
                                data_dict_income[eachelement['Fields']] = round(data_expense,2)

                            if data_dict_expense.get(eachelement['Fields']) is None:
                                data_dict_expense[eachelement['Fields']] = round(data_income,2)
                            try:
                                filter_data = AccountsModel.objects.filter(Q(Date__year=request.data['Year']) &
                                                                           Q(Date__month=request.data['Month']) &
                                                                           Q(user=request.data['UserId']) &
                                                                           Q(expenseApproved=True) &
                                                                           Q(Type=eachelement['Fields']))
                            finally:
                                if filter_data:
                                    Serializer_data = AccountsExpenseSerializer(filter_data, many=True)
                                    for eachelementinelement in Serializer_data.data:
                                        Data = eachelementinelement['Amount']
                                        if eachelementinelement['IsExpense'] is True:
                                            data_expense = data_expense + float(Data)
                                        else:
                                            data_income = data_income + float(Data)
                                    if data_expense:
                                        if data_dict_expense.get(eachelement['Fields']) is not None:
                                            data_dict_expense[eachelement['Fields']] =  round((data_dict_expense.get(eachelement['Fields']) + data_expense),2)
                                        else:
                                            data_dict_expense[eachelement['Fields']] =  round(data_expense,2)
                                    if data_income:
                                        if data_dict_income.get(eachelement['Fields']) is not None:
                                            data_dict_income[eachelement['Fields']] = round(data_dict_income.get(eachelement['Fields']) + data_income,2)
                                        else:
                                            data_dict_income[eachelement['Fields']] = round(data_income, 2)

                        list_dict.append(data_dict_income)
                        list_dict.append(data_dict_expense)
                        #data_total = {data_dict_income, data_dict_expense}
                        #income_s_dict = {data_dict_income_total, data_dict_income}

                        return Response(list_dict, status=status.HTTP_200_OK)

                return Response("USer ID or building name incorrect", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = UserInfo.objects.get(user=request.user)
        filter_data = ""
        Serializer_data =""
        Dropdown = Description.objects.all()
        serializer = AccountsDescriptionSerializer(Dropdown, many=True)
        ite = 0
        ite = ite + 1
        data_expense = 0
        data_income = 0
        try:
            filter_data = AccountsModel.objects.filter(Q(Date__year=request.data['Year']) &
                                                           Q(Date__month=request.data['Month']) &
                                                           Q(user=request.data['UserId']) &
                                                           Q(expenseApproved=True) )

        finally:
            if filter_data:
                #workbook = xlsxwriter.Workbook('accounts.xlsx')
                name = "accounts.xlsx"
                f = BytesIO()  # create a file-like object
                workbook = xlsxwriter.Workbook(f)
                worksheet = workbook.add_worksheet()
                row = 0
                col = 0
                Serializer_data = AccountsExportSerializer(filter_data, many=True)
                Row_1 = {'1': 'userID', '2':'Type of Account', '3':'Amount in INR', '4':'Expense',
                         '5':'Building Name', '6':'Unit Number', '7':'Date of Expenditure'}
                cell_format = workbook.add_format({'bold': True, 'text_wrap': True})
                for key in Row_1.keys():
                    worksheet.write(row, col, Row_1[key], cell_format)
                    col += 1
                for eachelement in Serializer_data.data:
                    col =0
                    cell_format = workbook.add_format({'text_wrap': True})
                    for key in eachelement.keys():
                        worksheet.write(row+1, col, eachelement[key],cell_format)
                        col +=1
                    row += 1
                workbook.close()
                Salutation = "Details of your account"
                Message  = "Hello " + str(request.user.username) + ",\n" \
                                                                      "PFA the account details for the month of " \
                           + str(request.data['Month']) + " in " + \
                           str(request.data['Year'])+"\n"+"This is an auto generated email, Do not reply \n\n\nRegards\nVD."
                message = EmailMessage(Salutation, Message, "virtualdoorsu@gmail.com", [str(request.user.email)],["murthy605@gmail.com","arunva28@gmail.com"])
                message.attach('accounts.xlsx', f.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                message.send()

                return Response("Mail with attachment sent to your email ID", status=status.HTTP_200_OK)
            else:
                return Response("Incorrect",status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='get')
class AllAccountsView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):
        #if user.is
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        if is_admin is True:
            accounts_info = AccountsModel.objects.all()
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            email = request.user.email
            accounts_info = AccountsModel.objects.filter(user=email)
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


