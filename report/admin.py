from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import *
from import_export.admin import ImportExportModelAdmin, ExportMixin, ImportMixin

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
   pass


@admin.register(Pastor)
class PastorAdmin(ImportExportModelAdmin):
   pass



class AppUserAdminForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'
    
    def clean(self):
        # Bypass all password validation
        return self.cleaned_data


class AppUserAdmin(UserAdmin):
    form = AppUserAdminForm
    add_form = AppUserAdminForm
    
    # Fix: Add proper ordering using an existing field (contact)
    ordering = ('contact',)  # Changed from username to contact
    
    # Fix: Define list_display to show important fields
    list_display = ('contact', 'name', 'church', 'department', 'is_staff', 'is_active')
    
    # Add list_filter if needed
    list_filter = ('is_staff', 'is_active', 'church', 'department')
    
    # Add search_fields for better search functionality
    search_fields = ('contact', 'name', 'church')
    
    # Your existing fieldsets
    fieldsets = (
        (None, {'fields': ('contact', 'department', 'password')}),
        ('Personal info', {'fields': ('name', 'church')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Your existing add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('church', 'department', 'contact', 'name', 
                      'is_local', 'is_district', 'is_officer', 
                      'is_active', 'is_staff'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new users
            obj.set_password(f"{obj.contact}{obj.department}")
        super().save_model(request, obj, form, change)

admin.site.register(AppUser, AppUserAdmin)