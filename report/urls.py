from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ( ActivityViewSet, BaptismViewSet, TransferViewSet, AttendanceViewSet, 
                        VisitorViewSet, DedicationViewSet, EventViewSet)
from django.shortcuts import redirect


from .view_table_dist import ( BaptismSummaryView_dist, TransferSummaryView_dist, 
                              AttendanceSummaryView_dist, VisitorMonthlySummaryView_dist, DedicationSummaryView_dist,
                              EventSummaryView_dist, ActivitySummaryView_dist)
                              
from .view_table_officer import ( BaptismSummaryView_of, TransferSummaryView_of, 
                              AttendanceSummaryView_of, VisitorMonthlySummaryView_of, DedicationSummaryView_of,
                              EventSummaryView_of, ActivitySummaryView_of 
                              
                              )


from .views_table_local import(ActivitySummaryView_local, VisitorSummaryView_local)

from .exporters import (export_church_data, get_model_fields,
                        export_data, get_model_fields_local,
                        get_model_fields_dist, export_data_dist)




from .views import (
    login_view, 
    LogoutView, 
    homepage_page_view, 
    submit_forms_page_view, 
    get_departments, 
    get_users,
    PageInDevelopment,
    dashboard_charts_page_view, 
    plotly_dashboard_charts_page_view,
    base_report_page_view,
    base_report_page_view_local,
    base_report_page_view_dist,
    base_report_page_view_officer,
    
)
# Create a router and register your viewset
router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'baptisms', BaptismViewSet)
router.register(r'transfers', TransferViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'dedications', DedicationViewSet)
router.register(r'events', EventViewSet)



urlpatterns = [
      path('admin_redirect/', lambda request: redirect('/admin/'), name='admin_redirect'),
      path('api/', include(router.urls)),  # Includes the API endpoints for activities
      path('', login_view, name='login'),
      path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
      path('homepage', homepage_page_view, name='homepage'),
      path('submit-forms', submit_forms_page_view, name='submitforms'),
      path('api/departments/', get_departments, name='get_departments'),
      path('get_users/', get_users, name='get_users'),
      path('get-model-fields/', get_model_fields, name='get_model_fields'),  # 🔥 Add this
      path('export_church_data/', export_church_data, name='export_church_data'),
     
      
      
    
      
      #local level url views
      path('reports/local/', base_report_page_view_local, name='report_dashboard_local'),
      path('reports/local/program-activity/', ActivitySummaryView_local.as_view(), name='activity_report_local'),
      path('reports/local/interest-cordinator/', VisitorSummaryView_local.as_view(), name='visitor_report_local'),
      path('export_data/', export_data, name='export_data'),
      path('get-model-fields-local/', get_model_fields_local, name='get_model_fields_local'),
      
      
      
      
      #district level views url
      path('reports/dist/', base_report_page_view_dist, name='report_dashboard_dist'),
      path('reports/dist/baptism/', BaptismSummaryView_dist.as_view(), name='baptism_report_dist'),
      path('reports/dist/transfer/', TransferSummaryView_dist.as_view(), name='transfer_report_dist'),
      path('reports/dist/attendance/', AttendanceSummaryView_dist.as_view(), name='attendance_report_dist'),
      path('reports/dist/visitors/', VisitorMonthlySummaryView_dist.as_view(), name='visitor_report_dist'),
      path('reports/dist/babydedication/', DedicationSummaryView_dist.as_view(), name='dedication_report_dist'),
      path('reports/dist/events/', EventSummaryView_dist.as_view(), name='event_report_dist'),
      path('reports/dist/program-activity/', ActivitySummaryView_dist.as_view(), name='activity_report_dist'),
      path('report/dist/export_data/', export_data_dist, name='export_data_dist'),
      path('get-model-fields-dist/', get_model_fields_dist, name='get_model_fields_dist'),
      
      
      #officers level url views
      path('reports/officer/', base_report_page_view_officer, name='report_dashboard_of'),
      path('reports/officer/baptism/', BaptismSummaryView_of.as_view(), name='baptism_report_of'),
      path('reports/officer/transfer/', TransferSummaryView_of.as_view(), name='transfer_report_of'),
      path('reports/officer/attendance/', AttendanceSummaryView_of.as_view(), name='attendance_report_of'),
      path('reports/officer/visitors/', VisitorMonthlySummaryView_of.as_view(), name='visitor_report_of'),
      path('reports/officer/babydedication/', DedicationSummaryView_of.as_view(), name='dedication_report_of'),
      path('reports/officer/events/', EventSummaryView_of.as_view(), name='event_report_of'),
      path('reports/officer/program-activity/', ActivitySummaryView_of.as_view(), name='activity_report_of'),
      path('report/dist/export_data/', export_data_dist, name='export_data_dist'),
      path('get-model-fields-dist/', get_model_fields_dist, name='get_model_fields_dist'),
        
     
      path("api/baptism-chart/", dashboard_charts_page_view, name="baptism_chart_data"),  
      path('plotly-dashboard/', plotly_dashboard_charts_page_view, name='plotly_dashboard'),
      
      
      
      
      path('in-development/', PageInDevelopment.as_view(), name='in-dev'),
     
      
]