from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    ConfirmSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    RestorePasswordSerializer)
from src.apps.users.models import Users, Code
from src.apps.users.task import send_html_email_task


class RegisterViewSet(viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_html_email_task(to=user.email, user_id=user.id)
        return Response({"message": "We Sent code to the Email"}, status=status.HTTP_201_CREATED)


class ConfirmViewSet(viewsets.GenericViewSet):
    queryset = Code.objects.all()
    serializer_class = ConfirmSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_obj = Code.objects.get(code=serializer.validated_data['code'])
        user = code_obj.user
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Code confirmed successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class ForgotPasswordViewSet(viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = ForgotPasswordSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = Users.objects.get(email=email)
        send_html_email_task(user.email, user.id)
        return Response({"We Sent code to email to verify email"}, status=status.HTTP_200_OK)


class RestorePasswordViewSet(viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = RestorePasswordSerializer

    def create(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error" : "Code is not Correct"})

        code_obj = Code.objects.get(code=code)
        if not code_obj:
            return Response({"error" : 'Invalid Code'})

        if code_obj.expired_time < timezone.now():
            return Response({"error" : "Code has expired"})

        user = code_obj.user

        serializer = self.get_serializer(data=request.data, context={'user' : user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message" : "Password updated successfully"}, status.HTTP_200_OK)



class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
