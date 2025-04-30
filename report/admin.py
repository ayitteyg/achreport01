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
    
    # Remove password fields from add/change forms
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'church', 'department', 'contact',  'name', 'is_local', 'is_district', 'is_officer', 'is_active', 'is_staff'),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('contact', 'department', 'password')}),
        ('Personal info', {'fields': ('name', 'church')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new users
            obj.set_password(f"{obj.contact}{obj.department}")
        super().save_model(request, obj, form, change)

admin.site.register(AppUser, AppUserAdmin)