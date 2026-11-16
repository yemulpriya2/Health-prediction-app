from datetime import date
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id", "full_name", "date_of_birth", "email",
            "glucose", "haemoglobin", "cholesterol", "remarks",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "remarks", "created_at", "updated_at"]


    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value
    

    def validate_email(self, value):
        return value.strip().lower()
    

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    

    def validate_glucose(self, value):
        if value < 0:
            raise serializers.ValidationError("Blood test value must be zero or greater.")
        return value
    

    def validate_haemoglobin(self, value):
        if value < 0:
            raise serializers.ValidationError("Blood test value must be zero or greater.")
        return value
    

    def validate_cholesterol(self, value):
        if value < 0:
            raise serializers.ValidationError("Blood test value must be zero or greater.")
        return value
