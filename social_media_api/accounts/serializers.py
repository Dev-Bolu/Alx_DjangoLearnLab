from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()  # dynamically get the active user model


# ------------------ USER REGISTRATION SERIALIZER ------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        """
        Create a new user using Django's built-in manager,
        then generate an authentication token.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
        )
        # create token for user
        Token.objects.create(user=user)
        return user


# ------------------ USER LOGIN SERIALIZER ------------------
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        data['user'] = user
        return data
