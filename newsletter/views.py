
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import NewsletterModel
from .serializers import NewsletterSerializer
from userinfo.models import UserInfo



# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@method_decorator(csrf_exempt, name='post')
class newsletterEdit(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request):
        staffInfo = NewsletterModel.objects.all()
        serializer = NewsletterSerializer(staffInfo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.user.email
        try:
            user = UserInfo.objects.get(user=email)
        finally:
            if user:
                is_admin = user.isAdmin
                if is_admin:
                    serializer = NewsletterSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=ValueError):
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    Response("Only admin can update Newsletters", status=status.HTTP_401_UNAUTHORIZED)

        return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='delete')
class NewsletterDelete(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    def delete(self, request, ID):
        user = UserInfo.objects.get(user=request.user)
        is_admin = user.isAdmin
        print(ID)
        if is_admin is True:
            try:
                field = NewsletterModel.objects.get(id=ID)
                field.delete()
                return Response("Deleted Successfully", status=status.HTTP_200_OK)
            except Description.DoesNotExist:
                return Response(" Not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)