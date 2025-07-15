from django.contrib.auth import logout
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, permissions, response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import views
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    ConfirmSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    RestorePasswordSerializer,
    LogoutSerializer
)
from src.apps.users.models import Users, Code
from src.apps.users.task import send_html_email_task
from .serializers import BecomeEntrepreneurSerializer
from src.apps.common.permissions import IsUserOnly
from src.apps.users.models.users import Role
from django.utils.translation import gettext_lazy as _


@extend_schema(tags=["Auth"])
class RegisterViewSet(viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_html_email_task(to=user.email, user_id=user.id)

        return Response({"message": _("We sent a confirmation code to your email.")}, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"])
class ConfirmViewSet(viewsets.GenericViewSet):
    serializer_class = ConfirmSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_obj = Code.objects.get(code=serializer.validated_data['code'])
        user = code_obj.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        code_obj.delete()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": _("Hisobingiz muvaffaqiyatli faollashtirildi."),
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class ForgotPasswordViewSet(viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = Users.objects.get(email=email)
        send_html_email_task(user.email, user.id)
        return Response({"message": _("We sent a code to your email to reset your password.")},
                        status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class RestorePasswordViewSet(viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = RestorePasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        code = request.data.get('code')
        if not code:

            return Response({"error": _("Code is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_obj = Code.objects.get(code=code)
        except Code.DoesNotExist:

            return Response({"error": _('Invalid Code.')}, status=status.HTTP_400_BAD_REQUEST)

        if code_obj.expired_time < timezone.now():

            return Response({"error": _("Code has expired.")}, status=status.HTTP_400_BAD_REQUEST)

        user = code_obj.user

        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        code_obj.delete()
        return Response({"message": _("Password updated successfully.")}, status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LogoutSerializer

    @action(detail=False, methods=["delete"])
    def logout(self, request):
        logout(request)
        return Response({"message": _("User logged out successfully.")}, status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class BecomeEntrepreneurAPIView(views.APIView):
    permission_classes = [IsAuthenticated, IsUserOnly]
    serializer_class = BecomeEntrepreneurSerializer

    def post(self, request):
        user = request.user
        user.role = Role.ENTREPRENEUR
        user.save()
        serializer = BecomeEntrepreneurSerializer(user)
        return Response({
            "message": _("You have successfully become an entrepreneur."),
            "data": serializer.data
        }, status.HTTP_200_OK)

@extend_schema(tags=["Auth"])
class GetUserDataViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
