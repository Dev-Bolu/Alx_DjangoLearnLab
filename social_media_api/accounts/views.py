from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    SimpleUserSerializer
)

User = get_user_model()

# ---------------------------------------------------------------------
# 🔹 REGISTER VIEW
# ---------------------------------------------------------------------
class RegisterView(APIView):
    """
    Handle user registration.
    Creates a new user, hashes password, and issues an auth token.
    """
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Registration successful',
                'user': SimpleUserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------
# 🔹 LOGIN VIEW
# ---------------------------------------------------------------------
class LoginView(APIView):
    """
    Handle user login.
    Authenticates using username/password and returns a token.
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'user': SimpleUserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------
# 🔹 USER PROFILE SERIALIZER
# ---------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio',
            'profile_picture', 'followers_count', 'following_count'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


# ---------------------------------------------------------------------
# 🔹 PROFILE VIEW
# ---------------------------------------------------------------------
class ProfileView(APIView):
    """
    Retrieve or update the current user's profile.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------
# 🔹 FOLLOW USER VIEW
# ---------------------------------------------------------------------
class FollowUserView(generics.GenericAPIView):
    """
    Authenticated user follows another user by ID.
    POST /api/accounts/follow/<int:user_id>/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        target = get_object_or_404(User, pk=user_id)
        if target in request.user.following.all():
            return Response({"detail": f"You already follow {target.username}."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target)
        serializer = SimpleUserSerializer(target, context={'request': request})
        return Response({
            "detail": f"You are now following {target.username}.",
            "user": serializer.data
        }, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------
# 🔹 UNFOLLOW USER VIEW
# ---------------------------------------------------------------------
class UnfollowUserView(generics.GenericAPIView):
    """
    Authenticated user unfollows another user by ID.
    POST /api/accounts/unfollow/<int:user_id>/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        target = get_object_or_404(User, pk=user_id)
        if target not in request.user.following.all():
            return Response({"detail": f"You are not following {target.username}."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)
        serializer = SimpleUserSerializer(target, context={'request': request})
        return Response({
            "detail": f"You have unfollowed {target.username}.",
            "user": serializer.data
        }, status=status.HTTP_200_OK)
