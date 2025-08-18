import logging
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, permissions, response, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from .serializers import (
    RegisterSerializer,
    ConfirmSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    RestorePasswordSerializer,
    LogoutSerializer,
    BecomeEntrepreneurSerializer
)
from src.apps.users.models import Users, Code
from src.apps.users.task import send_html_email_task
from src.apps.common.permissions import IsUserOnly
from src.apps.users.models.users import Role
from src.apps.common.pagination import CustomPagination

# Setup logger
logger = logging.getLogger(__name__)


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

        logger.info(f"[Auth] New user registered: {user.email} (id={user.id})")

        return Response({"message": _("We sent a confirmation code to your email.")}, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"])
class ConfirmViewSet(viewsets.GenericViewSet):
    serializer_class = ConfirmSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_obj = Code.objects.select_related('user').get(code=serializer.validated_data['code'])
        user = code_obj.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        code_obj.delete()
        refresh = RefreshToken.for_user(user)

        logger.info(f"[Auth] User confirmed account: {user.email} (id={user.id})")

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

        logger.info(f"[Auth] Password reset requested for {user.email}")

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
            logger.warning("[Auth] Restore password attempt without code")
            return Response({"error": _("Code is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_obj = Code.objects.get(code=code)
        except Code.DoesNotExist:
            logger.warning(f"[Auth] Invalid restore password code used: {code}")
            return Response({"error": _('Invalid Code.')}, status=status.HTTP_400_BAD_REQUEST)

        if code_obj.expired_time < timezone.now():
            logger.warning(f"[Auth] Expired code used for restore password by {code_obj.user.email}")
            return Response({"error": _("Code has expired.")}, status=status.HTTP_400_BAD_REQUEST)

        user = code_obj.user
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        code_obj.delete()

        logger.info(f"[Auth] Password successfully reset for {user.email} (id={user.id})")

        return Response({"message": _("Password updated successfully.")}, status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = Users.objects.all().order_by('id')
    pagination_class = CustomPagination

    def list(self, request):
        logger.info(f"[Auth] User list retrieved by {request.user}")
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if not page is None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @extend_schema(request=None, responses={200: None})
    @action(detail=False, methods=["delete"], url_path="logout")
    def logout(self, request):
        logger.info(f"[Auth] User {request.user} logged out")
        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK
        )


@extend_schema(tags=["Auth"])
class BecomeEntrepreneurAPIView(views.APIView):
    permission_classes = [IsAuthenticated, IsUserOnly]
    serializer_class = BecomeEntrepreneurSerializer

    def post(self, request):
        user = request.user
        user.role = Role.ENTREPRENEUR
        user.save()
        serializer = BecomeEntrepreneurSerializer(user)

        logger.info(f"[Auth] User {user.email} (id={user.id}) became an entrepreneur")

        return Response({
            "message": _("You have successfully become an entrepreneur."),
            "data": serializer.data
        }, status.HTTP_200_OK)


@extend_schema(tags=["Auth"])
class GetUserDataViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    @extend_schema(
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]
    )
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"[Auth] User data retrieved for {user.email} (id={user.id})")
        serializer = self.get_serializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
