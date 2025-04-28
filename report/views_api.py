from rest_framework import viewsets, permissions
from .models import Activity, Baptism, Transfer, Attendance, Visitor, Dedication
from .serializers import *#ActivitySerializer, BaptismSerializer, TransferSerializer, AttendanceSerializer, VisitorSerializer





class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def perform_create(self, serializer):
        serializer.save()  # Customize if you want to assign user

    def get_queryset(self):
        return Activity.objects.all()  # Modify if needed to filter activities per user
        # return Activity.objects.filter(user=self.request.user)  # Restrict users to their own activities



class BaptismViewSet(viewsets.ModelViewSet):
    queryset = Baptism.objects.all()  # You can customize the queryset if needed
    serializer_class = BaptismSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def perform_create(self, serializer):
        # You can customize the creation process if needed (e.g., assign a user or any other logic)
        serializer.save()

    def get_queryset(self):
        # You can modify this to filter the baptisms (e.g., based on the logged-in user)
        return Baptism.objects.all()  # Modify as needed for more advanced filtering
        # Example for user-specific filtering: 
        # return Baptism.objects.filter(user=self.request.user)  # if you have a user foreign key in the model
        
        
        
class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()  # You can customize the queryset if needed
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def perform_create(self, serializer):
        # You can customize the creation process if needed (e.g., assign a user or any other logic)
        serializer.save()

    def get_queryset(self):
        # You can modify this to filter the Transfer (e.g., based on the logged-in user)
        return Transfer.objects.all()  # Modify as needed for more advanced filtering
        # Example for user-specific filtering: 
        # return Transfer.objects.filter(user=self.request.user)  # if you have a user foreign key in the model
        


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Attendance.objects.all()
    


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        


class DedicationViewSet(viewsets.ModelViewSet):
    queryset = Dedication.objects.all()
    serializer_class = DedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes =  [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()