from django import forms
from django_select2.forms import Select2Widget
from .models import Activity, Baptism, Pastor, Transfer, Attendance, Visitor, Dedication, Event
import re

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['church', 'department', 'program', 'date', 'typ', 'facilitator', 'expense', 'income', 'rating']

        widgets = {
            'department': Select2Widget(attrs={'data-placeholder': 'Type to search...', 'style': 'width: 100%'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'style': 'resize: none;'}),
            'rating': forms.Select(choices=Activity._meta.get_field('rating').choices, attrs={'style': 'width: 100%'}),
        }

        
            # Adding help_text for rating field
        rating = forms.ChoiceField(
            choices=Activity._meta.get_field('rating').choices,
            required=False,
            help_text="Rate the activity on a scale of 1 to 5, where 1 is the lowest and 5 is the highest."
        )



class BaptismForm(forms.ModelForm):
    class Meta:
        model = Baptism
        fields = '__all__'  # Include all fields from the Baptism model
    

        
        widgets = {
                
                'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
                'date_church_voted': forms.DateInput(attrs={'type': 'date'}),
                'date_baptized': forms.DateInput(attrs={'type': 'date'}),
                
            }
    
    
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        print(f"Contact Input: {contact}")  # Debugging

        # Ensure contact is exactly 10 digits and contains only numbers
        if contact and not re.fullmatch(r"^\d{10}$", contact):
            raise forms.ValidationError("Contact number must be exactly 10 digits and contain only numbers.")

        return contact
        
        
    baptized_by = forms.ModelChoiceField(
        queryset=Pastor.objects.all(),  # Get all pastors from the Pastor model
        widget=Select2Widget(attrs={
            'data-placeholder': 'Type to search...', 
            'style': 'width: 100%;'
        }),
        empty_label="Select Pastor",  # Optional: Add an empty label for user guidance
    )
    

  


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = '__all__'  # Include all fields 
        widgets = {
                'date_church_voted': forms.DateInput(attrs={'type': 'date'}),
                
            }
     
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        print(f"Contact Input: {contact}")  # Debugging
        # Ensure contact is exactly 10 digits and contains only numbers
        if contact and not re.fullmatch(r"^\d{10}$", contact):
            raise forms.ValidationError("Contact number must be exactly 10 digits and contain only numbers.")
        return contact
        
   


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }
        
        


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if contact and (not contact.isdigit() or len(contact) != 10):
            raise forms.ValidationError("Contact number must be 10 digits.")
        return contact
    
    

class DedicationForm(forms.ModelForm):
    class Meta:
        model = Dedication
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



# forms.py
from django.contrib.auth.forms import AuthenticationForm

class PasswordlessAuthForm(forms.Form):
    department = forms.CharField()
    contact = forms.CharField()
    
    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        contact = cleaned_data.get('contact')
        
        if department and contact:
            # No password needed - we'll generate it automatically
            return cleaned_data
        raise forms.ValidationError("Both department and contact are required")