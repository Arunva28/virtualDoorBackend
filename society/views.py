
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Society_creategroupmodel, Society_memberaddmodel
from .serializers import SocietySerializer, GroupmemberSerializer
from userinfo.models import UserInfo
from django.core.mail import EmailMessage
from django.db.models import Q


# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@method_decorator(csrf_exempt, name='post')
class SocietyEdit(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):

        staffInfo = Society_creategroupmodel.objects.filter(groupaprrovedbybuildingadmin=True)
        serializer = SocietySerializer(staffInfo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.user.email
        try:
            user = UserInfo.objects.get(user=email)
        finally:
            if user:
                    request.data['mailid'] = email
                    print(request.data)
                    serializer = SocietySerializer(data=request.data)
                    if serializer.is_valid(raise_exception=ValueError):
                        serializer.save()

                        return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        user = ""
        field_to_update = request.data['id']
        try:
            field = Society_creategroupmodel.objects.get(id=field_to_update)
        finally:
            if field and field.mailid == request.user.email and field.adminofgroup == True:
                field.nameofgroup = request.data['nameofgroup']
                field.description = request.data['description']
                field.restrictedtomybuilding = request.data['restrictedtomybuilding']
                field.save()
                return Response("Updated", status=status.HTTP_200_OK)
            else:
                return Response("No ID found", status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='get')
class Societyapprovals(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):

        staffInfo = Society_creategroupmodel.objects.filter(groupaprrovedbybuildingadmin=False)
        serializer = SocietySerializer(staffInfo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request):
        user = ""
        try:
            user = UserInfo.objects.get(user=request.user)
        finally:
            is_admin = user.isAdmin
            valid_user =""
            response = ""
            if is_admin is False:
                return Response("Only admin can activate", status=status.HTTP_401_UNAUTHORIZED)
            field_to_update = request.data['id']
            try:
                field = Society_creategroupmodel.objects.get(id=field_to_update)
            finally:
                if field:
                    field.groupaprrovedbybuildingadmin = True
                    field.save()
                    content = {'group':field.nameofgroup, 'mailid': request.user.email,
                               'chat': 'Welcome admin', 'approvedbygroupadmin': True}
                    serializer = GroupmemberSerializer(data=content)
                    if serializer.is_valid(raise_exception=ValueError):
                        serializer.save()
                    return Response("Approved", status=status.HTTP_200_OK)
                else:
                    return Response("No ID found", status=status.HTTP_400_BAD_REQUEST)




@method_decorator(csrf_exempt, name='get')
class Societygroups(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):

        Mygroups = Society_memberaddmodel.objects.filter(mailid=request.user.email)
        serializer = GroupmemberSerializer(Mygroups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request):

        requesttojoin = Society_creategroupmodel.objects.filter((Q(nameofgroup=request.data['group']) & Q(groupaprrovedbybuildingadmin=True)))
        serializer_create = GroupmemberSerializer(requesttojoin, many=True)
        request.data['mailid'] = request.user.email
        serializer = GroupmemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            Salutation = "Dear" + str(serializer_create.data[0]['mailid'])
            Message =  "You have a new group request for" + str(request.data['group'])
            message = EmailMessage(Salutation, Message, "virtualdoorsu@gmail.com", [str(serializer_create.data[0]['mailid'])])
            message.send()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        members = Society_memberaddmodel.objects.filter(group=request.data['group'])
        serializer = GroupmemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='get')
class Mypage(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):

        Mygroups = Society_creategroupmodel.objects.filter((Q(mailid=request.user.email) & Q(adminofgroup=True)))
        serializer = SocietySerializer(Mygroups, many=True)
        data =[]
        if serializer.data is not None:
            for each in serializer.data:
                newrequests = Society_memberaddmodel.objects.filter(Q(group=each['nameofgroup'])& Q(approvedbygroupadmin=False))
                print(newrequests)
                serializer2 = GroupmemberSerializer(newrequests, many=True)
                data += serializer2.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("you are not admin of any group", status=status.HTTP_200_OK)

    def put(self,request):

        due  = Society_memberaddmodel.objects.get(id=request.data['id'])
        due.approvedbygroupadmin = True
        due.save()
        return Response("Approved", status=status.HTTP_200_OK)