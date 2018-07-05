from django.shortcuts import render
from .models import AccountsModel
from .serializers import AccountsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userinfo.models import UserInfo
from .models import Description
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


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
            accounts_info = AccountsModel.objects.filter(user=email)
            serializer = AccountsSerializer(accounts_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = ""
        valid_user = ""
        accounts = ""
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        if is_admin is True:
            try:
                valid_user = UserInfo.objects.get(user_id=request.data['user'])
            finally:
                if valid_user:
                    try:
                        accounts = Description.objects.get(Fields=request.data['Type'])
                    finally:
                        if accounts:
                            serializer = AccountsSerializer(data=request.data)
                            if serializer.is_valid(raise_exception=ValueError):
                                serializer.save()
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            print("Enter a valid Type of accounts")
                            return Response(status=status.HTTP_401_UNAUTHORIZED)

                else:
                    print("enter a valid user ID")
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)



