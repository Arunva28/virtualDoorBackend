from .serializers import TicketListSerializer, TicketDescriptionSerializer, TicketsNameSerializer
from .models import TicketDescription, TicketList, TicketsName
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from userinfo.models import UserInfo
from django.db.models import Q


# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@method_decorator(csrf_exempt, name='post')
class ComplaintsDropdownview(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = TicketsNameSerializer

    def get(self, request, format=None):
        complaints_list = TicketsName.objects.all()
        serializer = TicketsNameSerializer(complaints_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin

        if is_admin is True:
            TicketsName(TypeofIssue=request.data['NewIssue']).save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        field_to_delete = request.data['issue']
        field = TicketsName.objects.get(TypeofIssue=field_to_delete)
        if is_admin is True:
            try:
                field.delete()
                return Response("Field Deleted Successfully", status=status.HTTP_200_OK)
            except TicketsName.DoesNotExist:
                return Response("Field Not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class ComplaintsView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = TicketDescriptionSerializer

    def post(self, request, format=None):
        serializer = TicketDescriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            email = request.user.email
            user = UserInfo.objects.get(user=email)
            is_admin = user.isAdmin

            if is_admin is False:
                if request.data['Issue Resolved'] is False:
                    serializer.save()
                    ticket_details = TicketDescription.objects.filter(Description=request.data['Description'])
                    ticket_count = TicketDescription.objects.count()
                    ticket_count = ticket_count+1
                    ticket_details.TicketID = ticket_count
                    ticket_details.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("Update only unresolved complaints", status=status.HTTP_417_EXPECTATION_FAILED)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        email = request.user.email
        user = UserInfo.objects.get(user=email)
        is_admin = user.isAdmin
        if is_admin is True:
            complaints_list = TicketDescription.objects.filter(Q(BuildingName=user.buildingName) &
                                                               Q(IssueResolved=False))
            serializer = TicketDescriptionSerializer(complaints_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            complaints_list = TicketDescription.objects.filter(UserID=user.user)
            serializer = TicketDescriptionSerializer(complaints_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='post')
class UpdateStatus(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = TicketDescriptionSerializer

    def post(self, request):
        email = request.user.email
        user = UserInfo.objects.get(user=email)
        is_admin = user.isAdmin
        if is_admin is True:
            ticketdetails = TicketDescription.objects.get(id=request.data['ID'])
            if ticketdetails is not None:
                ticketdetails.IssueResolved = request.data['Complaint Status']
                ticketdetails.save()
                return Response("Ticket status updated", status=status.HTTP_200_OK)
            else:
                return Response("Incorrect TicketID", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Only building security can update status", status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='post')
class UpdateFeedback(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    serializer_class = TicketDescriptionSerializer

    def post(self, request):
        email = request.user.email
        user = UserInfo.objects.get(user=email)
        is_admin = user.isAdmin
        if is_admin is False:
            ticketdetails = TicketDescription.objects.get(id=request.data['ID'])
            print(ticketdetails)
            if ticketdetails is not None:
                ticketdetails.Feedback = request.data['Feedback']
                ticketdetails.save()
                return Response("Ticket status updated", status=status.HTTP_200_OK)
            else:
                return Response("Incorrect TicketID", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Only building users can update feedback", status=status.HTTP_401_UNAUTHORIZED)
