# resources/users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(APIView):
    def post(self, request):
        try:
            # Blacklist the refresh token
            token = request.data.get('refresh')
            if token is None:
                return Response({'detail': 'Refresh token is required.'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Blacklist the refresh token
            RefreshToken(token).blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({'detail': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
