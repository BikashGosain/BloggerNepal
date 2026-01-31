from rest_framework import serializers
from .models import AboutUs

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = (
            "id",
            "question",
            "answer",
            "created_at",
            "updated_at",
        )
