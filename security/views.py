from .serializers import SeurityOfficeSerializer, PrimaryKeyToSecuritySerializer
from .models import SecurityOffice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userinfo.models import UserInfo
from django.utils.dateparse import parse_date
from datetime import datetime
from datetime import timedelta
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@method_decorator(csrf_exempt, name='post')
class SecurityOfficeView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):
        email = request.user.email
        user = UserInfo.objects.get(user=email)
        is_admin = user.isAdmin
        if is_admin is True:
            securityofficeinfo = SecurityOffice.objects.all()
            var = SecurityOffice.objects.count()
            today = datetime.today()
            now = datetime.now()
            if var > 1:
                securityofficeinfo = SecurityOffice.objects.filter((Q(Date=today) & Q(Time__gte=now.time())) |
                                                                   Q(Date__gt=today)).order_by('Date', 'Time')
                serializer = SeurityOfficeSerializer(securityofficeinfo, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("No visitors", status=status.HTTP_200_OK)
        else:
            today = datetime.today()
            now = datetime.now()
            securityofficeinfo = SecurityOffice.objects.filter(((Q(Date=today) & Q(Time__gte=now.time())) |
                                                               Q(Date__gt=today)) &Q(user=email)).order_by('Date', 'Time')
            serializer = SeurityOfficeSerializer(securityofficeinfo, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = ""
        try:
            user = UserInfo.objects.get(user_id=request.data['user'])
        finally:
            if user:
                try:
                    str_Nowtime = request.data['Time']
                except:
                    Nowtime= datetime.now() + timedelta(minutes=5)
                    int_Nowtime="%02d:%02d:%02d" % (Nowtime.hour, Nowtime.minute, Nowtime.second)
                    str_Nowtime = str(int_Nowtime)
                    request.data['Time'] = str_Nowtime
                try:
                    Date = request.data['Date']
                except:
                    Date = datetime.now()
                    Date = Date.date()
                    Date = str(Date)
                    request.data['Date'] = Date
                Comparison_Date = Date.split('-')
                Integer_ComaprisonDate =[]

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
                ValidDate = 0x00;
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
                                        return Response("invalid date", status=status.HTTP_401_UNAUTHORIZED)
                                else:
                                    return Response("invalid date", status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            return Response("invalid date", status=status.HTTP_401_UNAUTHORIZED)




                ValidDate = 0x01;
                timefromAPI = datetime.now()
                int_timefromAPI = "%02d:%02d:%02d" % (timefromAPI.hour, timefromAPI.minute, timefromAPI.second)
                str_timefromAPI = str(int_timefromAPI)
                Comparison_time_from_API = str_timefromAPI.split(':')
                Comparison_time_received = str_Nowtime.split(':')

                l_Comaparison_fromAPI =[]
                l_Comparison_received =[]
                for i in range(0, len(Comparison_time_received)):
                    b = int(Comparison_time_received[i])
                    c = int(Comparison_time_from_API[i])
                    l_Comaparison_fromAPI.append(c)
                    l_Comparison_received.append(b)
                for i in range(0, 1):
                    if l_Comparison_received[0] > l_Comaparison_fromAPI[0]:
                        break
                    else:
                        if Integer_ComaprisonDate[0] > Date_Now[0] or (Integer_ComaprisonDate[1] > Date_Now[1]
                                                                       and Integer_ComaprisonDate[0] >= Date_Now[0])or \
                                (Integer_ComaprisonDate[2] > Date_Now[2] and Integer_ComaprisonDate[1] >= Date_Now[1]
                                 and Integer_ComaprisonDate[0] >= Date_Now[0]):
                            break
                        else:
                            if l_Comparison_received[0] == l_Comaparison_fromAPI[0]:
                                if l_Comparison_received[1] > l_Comaparison_fromAPI[1]:
                                    break
                                else:
                                    if l_Comparison_received[1] == l_Comaparison_fromAPI[1]:
                                        if l_Comparison_received[2] >= l_Comaparison_fromAPI[2]:
                                            break
                                        else:
                                            return Response("invalid time", status=status.HTTP_401_UNAUTHORIZED)
                                    else:
                                        return Response("invalid time", status=status.HTTP_401_UNAUTHORIZED)
                            else:
                                return Response("invalid time", status=status.HTTP_401_UNAUTHORIZED)

                serializer = PrimaryKeyToSecuritySerializer(data=request.data)

                if serializer.is_valid(raise_exception=ValueError):
                    email = request.user.email
                    user = UserInfo.objects.get(user=email)
                    is_admin = user.isAdmin
                    if is_admin is True:
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        user = request.data['user']
                        if email == user:
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response("Non-admin user cannot add other visitor", status=status.HTTP_401_UNAUTHORIZED)

                #else:
                 #   return Response("Datetime should be greater than current time", status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Test")
                return Response("User mail id is not valid", status=status.HTTP_401_UNAUTHORIZED)
