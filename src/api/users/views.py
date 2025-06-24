from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, ConfirmSerializer, UserSerializer
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
