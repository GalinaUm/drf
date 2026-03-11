from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar", "payments")
