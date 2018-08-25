from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userinfo.serializers import AddUserSerializer, BasicUserSerializer
from userinfo.models import UserInfo,BasicUserInfo
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# Create your views here.
@method_decorator(csrf_exempt, name='post')
class Registration(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def get(self, request, format=None):
        email = request.user.email
        user = BasicUserInfo.objects.get(email=email)
        is_superuser = user.is_superuser
        if is_superuser is True:
            users = UserInfo.objects.filter(isAdmin=True)
            serializer = AddUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("Not an admin")
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        email = request.user.email
        user = BasicUserInfo.objects.get(email=email)
        is_superuser = user.is_superuser
        if is_superuser is True:
            serializer = AddUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=ValueError):
                    unit_found = UserInfo.objects.all()
                    for count in unit_found:
                        if count.buildingName == request.data['buildingName']:
                            return Response("Building already registered", status=status.HTTP_417_EXPECTATION_FAILED)
                    print("im adding")
                    request.data['user']['username'] = request.data['user']['username'].lower()
                    request.data['user']['username'] = request.data['user']['username'].strip()
                    user = serializer.create(validated_data=request.data)
                    subject = 'Welcome to VirtualDoor'
                    message = 'Dear Customer,' + "\n" + 'Thank you for registering with us.' + "\n" + "\n" +\
                              'THIS IS AN AUTO GENERATED MAIL. PLEASE DO NOT REPLY TO THIS MAIL'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.data['user_id']]
                    send_mail(subject, message, email_from, recipient_list)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Not authorized", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class UpdateUserRights(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def post(self, request):
        email = request.user.email
        admin_status = BasicUserInfo.objects.get(email=email)
        if admin_status.is_superuser is True:
            current_user = request.data['email']
            try:
                user_info = BasicUserInfo.objects.get(email=current_user)
                user_info.is_superuser = request.data['is_superuser']
                user_info.save()
                return Response('Updated user admin rights', status=status.HTTP_200_OK)
            except:
                return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Non permissible',status=status.HTTP_401_UNAUTHORIZED)


# @method_decorator(csrf_exempt, name='post')
# class DeRegister(APIView):
#     authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
#     serializer_class = BasicUserSerializer
#
#     def post(self, request):
#         admin_email = request.user.email
#         user = BasicUserInfo.objects.get(email=admin_email)
#         if user.is_superuser is True:
#             try:
#                 print("i m here")
#                 user2 = UserInfo.objects.get(user=request.data['email'])
#                 userlist = UserInfo.objects.filter(Q(user2.buildingName))
#                 print(userlist)
#                 return Response("User Deleted Successfully", status=status.HTTP_200_OK)
#             except UserInfo.DoesNotExist:
#                 return Response("User Not found", status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)