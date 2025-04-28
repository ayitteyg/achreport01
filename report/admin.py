from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ExportMixin, ImportMixin

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
   pass


@admin.register(Pastor)
class PastorAdmin(ImportExportModelAdmin):
   pass