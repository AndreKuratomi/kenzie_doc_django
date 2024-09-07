from rest_framework import serializers

from .models import MailModel


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailModel
        fields = "__all__"
