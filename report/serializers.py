from rest_framework import serializers
from .models import Activity, Baptism, Transfer, Attendance, Visitor, Dedication, Event

class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)  # Replace user_id with username
    department = serializers.CharField(source="department.name", read_only=True)  # Replace department_id with name

    class Meta:
        model = Activity
        fields = [
            "id",
            "user",  # Replaces user_id
            "church",
            "department",  # Replaces department_id
            "program",
            "date",
            "typ",
            "facilitator",
            "expense",
            "income",
            "rating",
            "remarks",
        ]


class BaptismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baptism
        fields = "__all__"  # This will include all fields in the model automatically
        
    
class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"  # This will include all fields in the model automatically


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        
        
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"
        



class DedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dedication
        fields = "__all__"



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

