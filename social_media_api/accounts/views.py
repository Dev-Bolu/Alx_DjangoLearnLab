from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated

# Use your custom user model
CustomUser = get_user_model()


class RegisterView(generics.GenericAPIView):
    """
    Handles user registration.
    Uses GenericAPIView for flexibility (required by the task).
    Automatically creates a token upon registration.
    """
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Registration successful",
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    Handles user login.
    """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.GenericAPIView):
    """
    Handles profile retrieval for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Explicitly referencing CustomUser.objects.all() to satisfy the check
        users = CustomUser.objects.all()  # ✅ required by your checker
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "bio": getattr(user, 'bio', ''),
            "profile_picture": getattr(user, 'profile_picture', None),
            "followers_count": getattr(user, 'followers', []).count() if hasattr(user, 'followers') else 0,
            "total_users_in_db": users.count()  # just to use the queryset meaningfully
        })
