from .serializers import BasicUserSerializer, AddUserSerializer, ForgotPasswordSerializer
from .models import BasicUserInfo, UserInfo, ForgotPassword
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.core.mail import send_mail
from django.conf import settings
from django_otp.oath import TOTP
from django_otp.util import random_hex
import time
from datetime import datetime, timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from array import array

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# Create your views here.
@method_decorator(csrf_exempt, name='post')
class UserRecordView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def get(self, request, format=None):
        email = request.user.email
        user = UserInfo.objects.get(user=email)
        is_admin = user.isAdmin
        if is_admin is True:
            print("admin")
            print(user.buildingName)
            users = UserInfo.objects.filter(buildingName=user.buildingName)
            serializer = AddUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
             print("Not an admin")
             content = UserInfo.objects.filter(user_id=user.user_id)
             serializer = AddUserSerializer(content, many=True)
             return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        print(request.data['user'])

        email = request.user.email
        user = UserInfo.objects.get(user=email)
        is_admin = user.isAdmin
        if is_admin is True:
            serializer = AddUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=ValueError):
                if user.buildingName == request.data['buildingName']:
                    unit_found = UserInfo.objects.filter(Q(buildingName=request.data['buildingName']))
                    for element in unit_found:
                        if request.data['unitNo'] == element.unitNo:
                            tenant_found = UserInfo.objects.filter((Q(buildingName=request.data['buildingName'])
                                                                   & Q(unitNo=request.data['unitNo'])))

                            for count in tenant_found:
                                if request.data['houseNo'] == count.houseNo:
                                    return Response("Tenant already exists. Please verify", status=status.HTTP_400_BAD_REQUEST)
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
                    return Response("unitNo does not exist", status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response("Building Names do not match", status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Not authorized", status=status.HTTP_401_UNAUTHORIZED)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        request.data['username'] = request.data['username'].lower()
        request.data['username'] = request.data['username'].strip()

        data1 = request.data
        username = data1['username']
        password = data1['password']

        valid_user = authenticate(username=username, password=password)
        if valid_user is not None:
            login(request, valid_user)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_info = UserInfo.objects.get(user_id=user)
            phone = (str(user_info.phoneNo))
            content = {
                'token': token.key, 'user_id': user.pk, 'email': user.email, 'phoneNo': phone,
                'building_name': user_info.buildingName, 'unit_no': user_info.unitNo, 'is_Admin': user_info.isAdmin

            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)


@login_required
@api_view(['POST', 'GET'])
def user_logout(request):
    print("logging off")
    logout(request)
    return Response("You are logged out")


@method_decorator(csrf_exempt, name='delete')
class UserOperations(APIView):
    print("tillhere")
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = BasicUserSerializer

    def delete(self, request, email):
        admin_email = request.user.email
        user = UserInfo.objects.get(user=admin_email)
        is_admin = user.isAdmin
        if is_admin is True:
            try:
                user = BasicUserInfo.objects.get(email=email)
                user.delete()
                return Response("User Deleted Successfully", status=status.HTTP_200_OK)
            except BasicUserInfo.DoesNotExist:
                return Response("User Not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class OTPVerification(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data['email']
        user = ForgotPassword.objects.get(user_email=email)
        user2 = BasicUserInfo.objects.get(email=email)
        if user is not None:
            try:
                token = request.data['token']
                # convert the input token to integer
                token = int(token)
                current_time = datetime.now(timezone.utc)
                print(user.date_time)
                print(current_time)

                if current_time < user.date_time + timedelta(minutes=5):
                    if token == user.otp:
                        if request.data['new_password'] != request.data['confirm_password']:
                            return Response("Passwords do not match", status=status.HTTP_400_BAD_REQUEST)
                        else:
                            user2.password = make_password(request.data['new_password'])
                            user2.save()
                            logout(request)
                            return Response("Password changed successfully. Please login again with new password",
                                            status=status.HTTP_200_OK)
                    else:
                        return Response("Wrong Token", status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response("Time lapsed", status=status.HTTP_401_UNAUTHORIZED)
            except ValueError:
                return Response("invalid")
        else:
            return Response("User Not Found", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class OTPGeneration(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        print("till post")

        email = request.data['email']
        try:
            user = BasicUserInfo.objects.get(email=email)

            if user is not None:
                print("till user")
                totp = self.totp_obj()
                token = str(totp.token()).zfill(6)
                req_data = dict({'user_email': email,
                             'otp': token,
                             'date_time': datetime.now(timezone.utc)
                             })
                try:
                    user = ForgotPassword.objects.get(user_email=email)
                    user.delete()
                except:
                    print("user not available")
                forgot_password_serializer = ForgotPasswordSerializer(data=req_data)
                if forgot_password_serializer.is_valid(raise_exception=ValueError):
                    forgot_password_serializer.save()
                    subject = 'Forgot Your Password?'
                    message = 'Dear Customer,' + "\n" + \
                                'We wanted to inform you that we have received your password change request.' \
                                'This email contains OTP for password change' + "\n" + "\n" + \
                                'OTP : ' + token + "\n"' Please note that this is valid only for 5 minutes'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list)
                    return Response("Mail sent successfully. Please check your inbox", status=status.HTTP_200_OK)
                else:
                    return Response("Invalid Format", status=status.HTTP_400_BAD_REQUEST)

        except:
            print("till nowhere")
            return Response("User Not found in database", status=status.HTTP_400_BAD_REQUEST)

    def totp_obj(self):
        totp = TOTP(key=random_hex(20),
                    step=300,
                    digits=6)
        totp.time = time.time()
        return totp


@method_decorator(csrf_exempt, name='post')
class UpdatePassword(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def post(self, request):
        for eachelement in BasicUserInfo.objects.all():
            user = str(eachelement)
            if user == request.user.username:
                if request.data['NewPassword'] != request.data['ConfirmPassword']:
                    return Response("New password and confirm password are not similar", status=status.HTTP_400_BAD_REQUEST)

                oldpassword = request.data['Oldpassword']
                database = str(eachelement.password)
                success = check_password(oldpassword, database)
                if success:
                    if request.data['Oldpassword'] == request.data['NewPassword']:
                        return Response("New password cannot be same as old password",
                                        status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif "" == request.data['NewPassword']:
                        return Response(" Password cannot be blank", status=status.HTTP_400_BAD_REQUEST)
                    else:
                        eachelement.password = make_password(request.data['NewPassword'])
                        eachelement.save()
                        logout(request)
                        return Response("Password Changed Successfully, Login again with new password",
                                        status=status.HTTP_200_OK)
                else:
                    return Response("Incorrect Password", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Invalid User", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class UpdateMobileNumber(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def post(self, request):
        email = request.user.email
        user_details = UserInfo.objects.get(user=email)
        if user_details is not None:

            old_number = request.data['Old_Number']
            phone_no = user_details.phoneNo
            if old_number == phone_no:
                if request.data['Old_Number'] == request.data['NewNumber']:
                    return Response("New number cannot be same as old number", status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    user_details.phoneNo = (request.data['NewNumber'])
                    user_details.save()
                    return Response("Phone Number updated", status=status.HTTP_200_OK)
            else:
                return Response("Incorrect PhoneNo", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Invalid User", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class UpdateAdminRights(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def post(self, request):
        email = request.user.email
        admin_status = UserInfo.objects.get(user=email)
        if admin_status.isAdmin is True:
            current_user = request.data['user']
            try:
                user_info = UserInfo.objects.get(user=current_user)

                user_info.isAdmin = request.data['isAdmin']
                user_info.save()
                return Response('Updated user admin rights', status=status.HTTP_200_OK)
            except:
                return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Non permissible',status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class UpdateHouseNo(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def post(self, request):
        email = request.user.email

        admin_status = UserInfo.objects.get(user=email)
        if admin_status.isAdmin is True:
            current_user = request.data['user']
            try:
                user_info = UserInfo.objects.get(user=current_user)
                vacant_status = UserInfo.objects.filter(Q(buildingName=admin_status.buildingName)
                                                    & Q(unitNo=request.data['unitNo']))
                for count in vacant_status:
                    if request.data['houseNo'] == count.houseNo:
                        return Response("Tenant already exists. Please verify", status=status.HTTP_400_BAD_REQUEST)
                user_info.houseNo = request.data['houseNo']
                user_info.unitNo = request.data['unitNo']
                user_info.save()
                return Response('Updated house No', status=status.HTTP_200_OK)
            except:
                return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Non permissible',status=status.HTTP_401_UNAUTHORIZED)


class UnitNoQuery(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def get(self, request):
        unitnumbers = []
        serializer = AddUserSerializer(data=request.data)
        email = request.user.email
        user = UserInfo.objects.get(user=email)

        users = UserInfo.objects.filter(buildingName=user.buildingName)
        for eachelement in users:
            unitnumbers.append(eachelement.unitNo)
        return Response(unitnumbers, status=status.HTTP_200_OK)


class HouseNoQuery(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = AddUserSerializer

    def get(self, request):
        housenumbers = []
        serializer = AddUserSerializer(data=request.data)
        email = request.user.email
        user = UserInfo.objects.get(user=email)

        users = UserInfo.objects.filter(buildingName=user.buildingName)
        for eachelement in users:
            housenumbers.append(eachelement.houseNo)
        return Response(housenumbers, status=status.HTTP_200_OK)
