# resources/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid email or password.')

        attrs['user'] = user
        return attrs
