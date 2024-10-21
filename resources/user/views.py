# resources/users/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


class LoginView(generics.GenericAPIView):
    """
    Handles user login requests by validating credentials and providing
    authentication tokens.

    This view processes POST requests where users submit their login
    credentials. If valid, the user is authenticated, and both refresh and
    access tokens are returned in the response.

    Features:
    - Rate limited to prevent abuse: Limits login attempts to 5 per minute per
      user or IP address.
    - Utilizes Django REST Framework's `GenericAPIView` for handling the view
      logic.
    - Returns JWT tokens for user authentication.

    Attributes:
    - serializer_class: Defines the serializer used to validate login data
      (LoginSerializer).
    - permission_classes: Allows unauthenticated users to access this view
      (permissions.AllowAny).

    Methods:
    - post(request, *args, **kwargs): Processes the login request, validates
      user credentials,
      and generates JWT tokens (access and refresh).
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='user_or_ip', rate='5/m', block=True))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Create tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(generics.GenericAPIView):
    """
    API view to handle user logout by blacklisting the refresh token.

    This view allows authenticated users to log out by providing a
    refresh token. When the refresh token is valid, it will be
    blacklisted, preventing it from being used for further authentication.

    Methods
    -------
    post(request):
        Handles POST requests to blacklist the provided refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token
            token = request.data.get('refresh')
            if token:
                # Validate the refresh token
                if not RefreshToken(token).token:
                    return Response({"detail": "Invalid token"}, status=400)
                RefreshToken(token).blacklist()
                return Response(
                    {"message": "Refresh token successfully blacklisted."},
                    status=205)
            else:
                return Response({"error": "Invalid or missing refresh token."},
                                status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
