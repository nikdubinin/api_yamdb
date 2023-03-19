from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from users.permissions import IsAdmin
from users.serializers import (
    ConfirmationSerializer, SignUpSerializer, UserSerializer,
    NotAdminUserSerializer, User
)
from .utils import uuid, send_confirmation_code


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        send_confirmation_code(
            request.data['username'],
            request.data['email']
        )
        return Response(
            request.data, status=status.HTTP_200_OK
        )
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    try:
        User.objects.create(
            **serializer.validated_data,
            confirmation_code=confirmation_code
        )
    except Exception as error:
        return Response(
            f'Произошла ошибка {error}',
            status=status.HTTP_400_BAD_REQUEST
        )
    send_confirmation_code(
        username,
        serializer.validated_data['email'],
        confirmation_code=confirmation_code
    )
    return Response(
        serializer.data, status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdmin,
    )
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ('post', 'get', 'head', 'patch', 'delete')
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = NotAdminUserSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
