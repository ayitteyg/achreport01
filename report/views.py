
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views import generic, View
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .drive_service import upload_json_to_drive
from django.views.generic import TemplateView
from .forms import (ActivityForm, BaptismForm, TransferForm, AttendanceForm,
                    VisitorForm, DedicationForm, EventForm, TreasuryForm )# Add all forms you need
from django.http import JsonResponse
from .models import Department, Activity, Baptism, Transfer, Attendance, Visitor, Dedication, Event, Treasury
from django.contrib.auth import get_user_model
import json
from django.contrib.auth.decorators import login_required
#import pandas as pd
#from django_plotly_dash import DjangoDash
#3import plotly.express as px
from .functions import (years, months, quarters, 
                        reset_model_data, 
                        print_model_objects,
                        convert_to_json, load_json_model)
from .ploty_dash import create_bar_chart, get_bar_data

from django.db.models import Count
from .bulk_data_test import run_data

User = get_user_model()

#run_data()

# deleted_count, deletion_details = reset_model_data(Baptism)
# print(f"Deleted {deleted_count} records from {Baptism.__name__}")
#print_model_objects(Treasury)

# Get all usernames as a list
#usernames = list(User.objects.values_list('contact', flat=True))

#print(usernames)

#reset_model_data(Treasury)
# Reset all data in MyModel
#convert_to_json(file='treasury')
#load_json_model(file='treasury', model=Treasury)




class CustomLoginView(View):
    template_name = 'root/login.html'
    redirect_authenticated_user = True
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.redirect_authenticated_user:
            return redirect(self.get_success_url())
        return render(request, self.template_name)
    
    
    def post(self, request, *args, **kwargs):
        department = request.POST.get('username')
        contact = request.POST.get('password')
        
        #print(department)
        #print(contact)
        
        if not department or not contact:
            return redirect('login_failed')
        
        user = PasswordlessAuthBackend().authenticate(
            request,
            department=department,
            contact=contact
        )
        
        if user is not None:
            login(request, user, backend='report.auth_backends.PasswordlessAuthBackend')
            return redirect(self.get_success_url())
        
        return redirect('login_failed')
    
    def get_success_url(self):
        return reverse_lazy('homepage')
login_view = CustomLoginView.as_view()



from .forms import PasswordlessAuthForm
from .auth_backends import PasswordlessAuthBackend
class CustomLoginView(FormView):
    template_name = 'root/login.html'
    form_class = PasswordlessAuthForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('homepage')
    
    def form_valid(self, form):
        department = form.cleaned_data['department']
        contact = form.cleaned_data['contact']
        
        #print(department)
        #print(contact)
        
        # Authenticate using our custom backend
        user = PasswordlessAuthBackend().authenticate(
            self.request,
            department=department,
            contact=contact
        )
        
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return redirect('login_failed')
login_view2 = CustomLoginView.as_view()




def login_failed_view(request):
    return render(request, 'root/login_fail.html')


class HomepageView(TemplateView):
    template_name = 'root/homepage.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            if user.is_local:
                context['report_url'] = reverse("report_dashboard_local")
            elif user.is_district:
                context['report_url'] = reverse("report_dashboard_dist")
            elif user.is_officer:
                context['report_url'] = reverse("report_dashboard_officer")
            else:
                context['report_url'] = reverse("homepage")
        else:
            context['report_url'] = reverse("login")

        return context
    
homepage_page_view = HomepageView.as_view() 




# @login_required

def get_users(request):
    query = request.GET.get("q", "")
    User = get_user_model()
    users = User.objects.filter(username__icontains=query).values_list("username", flat=True)[:5]
    return JsonResponse(list(users), safe=False)



#api endpoint to fetch department
def get_departments(request):
    query = request.GET.get("q", "")
    departments = Department.objects.filter(name__icontains=query).values_list("name", flat=True)
    return JsonResponse(list(departments), safe=False)


class SubmitFormsView(generic.TemplateView):
    template_name = 'page/submit_form.html'
    login_url = 'login'  # Redirect to login page if not authenticated

    form_classes = {
        "activity": ActivityForm,
        "baptism": BaptismForm,
        "transfer": TransferForm,
        "attendance": AttendanceForm,
        "visitor": VisitorForm,
        "dedication": DedicationForm,
        "event": EventForm,
        "treasury":TreasuryForm,
    }

    form_info = [
        {
            "name": "Activity", "icon": "bi-graph-up-arrow",
            "description": "Record departmental programs, type, and financial data for each activity.",
            "form_key": "activity"
        },
        {
            "name": "Baptism", "icon": "bi-droplet",
            "description": "Submit baptism records including names, date baptized, and officiating pastor.",
            "form_key": "baptism"
        },
        {
            "name": "Transfer", "icon": "bi-arrow-left-right",
            "description": "Manage incoming and outgoing member transfers voted by the church.",
            "form_key": "transfer"
        },
        {
            "name": "Attendance", "icon": "bi-person-check",
            "description": "Track weekly attendance for adults, youth, children, and combined services.",
            "form_key": "attendance"
        },
        {
            "name": "Visitor", "icon": "bi-person-plus",
            "description": "Log visitors to the church with their name, contact, and Adventist status.",
            "form_key": "visitor"
        },
        {
            "name": "Dedication", "icon": "bi-person-heart",
            "description": "Submit baby dedication records including parents and child details.",
            "form_key": "dedication"
        },
        {
            "name": "Event", "icon": "bi-calendar-event",
            "description": "Record special church events like marriages, funerals, others.",
            "form_key": "event"
        },
        
        {
            "name": "Treasury", "icon": "bi-cash-stack",
            "description": "Record summary treasury activities; tithe, combined, and other offerings.",
            "form_key": "treasury"
        },
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, form_class in self.form_classes.items():
            context[f'{key}_form'] = form_class()
        context['form_info'] = self.form_info
       # print(context)
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        for key, form_class in self.form_classes.items():
            context[f'{key}_form'] = form_class(request.POST)

        for key, form in context.items():
            if isinstance(form, (ActivityForm, BaptismForm, TransferForm, AttendanceForm, 
VisitorForm, DedicationForm, EventForm, TreasuryForm)) and form.is_valid():
                
                #print(form)
                
                instance = form.save(commit=False)
                instance.user = request.user
                
                #print('user')
                #print(instance.user)
                
                instance.save()

                # Upload corresponding data to Google Drive
                model_map = {
                    'activity_form': (Activity, 'activities.json'),
                    'baptism_form': (Baptism, 'baptisms.json'),
                    'transfer_form': (Transfer, 'transfers.json'),
                    'attendance_form': (Attendance, 'attendances.json'),
                    'visitor_form': (Visitor, 'visitors.json'),
                    'dedication_form': (Dedication, 'dedications.json'),
                    'event_form': (Event, 'events.json'),
                    'treasury_form': (Treasury, 'treasury.json'),
                }

                model_class, filename = model_map[key]
                data = list(model_class.objects.values())
                #upload_json_to_drive(filename, data)

                if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"message": "Report submitted successfully!"})
                return redirect('/')

        # If no form is valid, return the first form's errors
        for form in context.values():
            #print()
            #print(" contect values",context.values())
            if hasattr(form, 'errors') and form.errors:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"errors": form.errors}, status=400)

        return self.render_to_response(context)

submit_forms_page_view = SubmitFormsView.as_view()






class ReportDashboardViewLocal(View):
    def get(self, request):
        user = self.request.user
        print(user)
       
        context = {
            "user": user,
        }
        return render(request, 'reports/local/base_report.html', context)  
base_report_page_view_local = ReportDashboardViewLocal.as_view()





class ReportDashboardViewDist(View):
    def get(self, request):
        return render(request, 'reports/district/base_report.html') 
base_report_page_view_dist = ReportDashboardViewDist.as_view()



class ReportDashboardViewOfficer(View):
    def get(self, request):
        return render(request, 'reports/officer/base_report.html')   
base_report_page_view_officer = ReportDashboardViewOfficer.as_view()





class ReportDashboardView(View):
    def get(self, request):
        user = self.request.user
        print(user)
       
        context = {
            "user": user,
        }
        return render(request, "reports/base_report.html", context)
base_report_page_view = ReportDashboardView.as_view()


















class BaptismReportView(View):
    def get(self, request, *args, **kwargs):
        # Get the filter options from the GET request or set defaults
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        quarter = request.GET.get('quarter', None)
        
        # Initialize querysets 
        baptisms = Baptism.objects.all()

        # Filter by year if provided
        if year:
            try:
                year = int(year)
                baptisms = baptisms.filter(date_baptized__year=year)
            except ValueError:
                pass  # If the year is not a valid integer, skip this filter

        # Filter by month if provided
        if month not in [None, '', 'None']:
            month = int(month)
            baptisms = baptisms.filter(date_baptized__month=month)
          
        # Filter by quarter if provided
        if quarter:
            try:
                quarter = int(quarter)
                if quarter == 1:
                    baptisms = baptisms.filter(date_baptized__month__in=[1, 2, 3])
                elif quarter == 2:
                    baptisms = baptisms.filter(date_baptized__month__in=[4, 5, 6])
                elif quarter == 3:
                    baptisms = baptisms.filter(date_baptized__month__in=[7, 8, 9])
                elif quarter == 4:
                    baptisms = baptisms.filter(date_baptized__month__in=[10, 11, 12])
            except ValueError:
                pass

        # Group by church_baptized_into and count baptisms
        baptism_counts = baptisms.values('church_baptized_into').annotate(baptism_count=Count('id'))
        total_baptism_count = baptisms.aggregate(total_baptisms=Count('id'))['total_baptisms']  # Calculate the total count

        # Prepare chart data
        baptism_data = get_bar_data(x_field='church_baptized_into', y_field='baptism_count',
                                     data=baptism_counts, x_title='Church', y_title='Number of Baptisms')

        # Prepare charts list to pass multiple charts
        charts = [
            {'id': 'baptism_json', 'data': json.dumps(baptism_data), 'name': 'Baptism', 'total': total_baptism_count},
        ]

        
        # Render the dashboard with the charts
        context = {
            "charts": charts,
            'year': year,
            'month': month,
            'quarter': quarter,
            'years':years,
            'months': months,
            'quarters': quarters,
        }

        return render(request, 'reports/baptism_report.html', context)


















class PageInDevelopment(View):
    def get(self, request):
        context = {}
        return render(request, 'page/page_in_development.html', context)



class AttendanceReportView(View):
    def get(self, request):
        context = {'report':'attendance reports'}
        return render(request, 'reports/attendance_report.html', context)


class TransferReportView(View):
    def get(self, request):
        context = {'report':'transfer reports'}
        return render(request, 'reports/transfer_report.html', context)
    
    
    




























































































#chart & Report
class ChartsDashboardView(TemplateView):
    template_name = 'page/dashboard_charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        print("view is rendered")

        # Baptism Chart Data
        baptism_data = Baptism.objects.values("church_baptized_into").annotate(total=Count("id"))
        baptism_chart = {
            "labels": [d["church_baptized_into"] for d in baptism_data],
            "datasets": [{
                "label": "Baptisms",
                "data": [d["total"] for d in baptism_data],
                "backgroundColor": "#0d6efd"
            }]
        }

        # You can add more chart data here
        # e.g., another chart (mock)
        another_chart = {
            "labels": ["A", "B", "C"],
            "datasets": [{
                "label": "Another Metric",
                "data": [3, 5, 2],
                "backgroundColor": "#198754"
            }]
        }

        # Pass JSON-serialized charts to the template
        context["charts"] = {
            "baptismChart": json.dumps(baptism_chart),
            "anotherChart": json.dumps(another_chart),
        }
        print(context)
        print("Nothing in context")
        return context
    
dashboard_charts_page_view = ChartsDashboardView.as_view()


#plotly-dash-report

class PlotlyDashboardView(View):
    def get(self, request, *args, **kwargs):
        # Get the filter options from the GET request or set defaults
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        quarter = request.GET.get('quarter', None)
        

        # Initialize querysets 
        baptisms = Baptism.objects.all()
        transfers_in = Transfer.objects.filter(typ="transfer_in")
        transfers_out = Transfer.objects.filter(typ="transfer_out")
        

        # Filter by year if provided
        if year:
            try:
                year = int(year)
                baptisms = baptisms.filter(date_baptized__year=year)
                transfers_in = transfers_in.filter(date_church_voted__year=year)
                transfers_out = transfers_out.filter(date_church_voted__year=year) 
            except ValueError:
                pass  # If the year is not a valid integer, skip this filter

        # Filter by month if provided
        if month not in [None, '', 'None']:
            month = int(month)
            baptisms = baptisms.filter(date_baptized__month=month)
            transfers_in = transfers_in.filter(date_church_voted__month=month)
            transfers_out = transfers_out.filter(date_church_voted__month=month)

        # Filter by quarter if provided
        if quarter:
            try:
                quarter = int(quarter)
                if quarter == "1":
                    baptisms = baptisms.filter(date_baptized__month__in=[1, 2, 3])
                    transfers_in = transfers_in.filter(date_church_voted__month__in=[1, 2, 3])
                    transfers_out = transfers_out.filter(date_church_voted__month__in=[1, 2, 3])
                    
                elif quarter == "2":
                    baptisms = baptisms.filter(date_baptized__month__in=[4, 5, 6])
                    transfers_in = transfers_in.filter(date_church_voted__month__in=[4,5,6])
                    transfers_out = transfers_out.filter(date_church_voted__month__in=[4,5,6])
                    
                elif quarter == "3":
                    baptisms = baptisms.filter(date_baptized__month__in=[7, 8, 9])
                    transfers_in = transfers_in.filter(date_church_voted__month__in=[7,8,9])
                    transfers_out = transfers_out.filter(date_church_voted__month__in=[7,8,9])
                    
                elif quarter == "4":
                    baptisms = baptisms.filter(date_baptized__month__in=[10, 11, 12])
                    transfers_in = transfers_in.filter(date_church_voted__month__in=[10,11,12])
                    transfers_out = transfers_out.filter(date_church_voted__month__in=[10,11,12])
                    
            except ValueError:
                pass
        # Group by church_baptized_into and count baptisms
        baptism_counts = baptisms.values('church_baptized_into').annotate(baptism_count=Count('id'))
        total_baptism_count = baptisms.aggregate(total_baptisms=Count('id'))['total_baptisms'] # Calculate the total count
        
        
        transfersin_counts = transfers_in.values('church').annotate(transferin_count=Count('id'))
        total_transfersin = transfers_in.aggregate(total_transfersin=Count('id'))['total_transfersin'] # Calculate the total count
        
        transfersout_counts = transfers_out.values('church').annotate(transferout_count=Count('id'))
        total_transfersout = transfers_out.aggregate(total_transfersout=Count('id'))['total_transfersout'] # Calculate the total count
       

        # Prepare  chart data
        baptism_data = get_bar_data(x_field='church_baptized_into', y_field='baptism_count',
                                    data=baptism_counts, x_title='church', y_title='Number of Baptism')
        
        transferin_data = get_bar_data(x_field='church', y_field='transferin_count',
                                    data=transfersin_counts, x_title='church', y_title='Number of Transfers in')
        
        transferout_data = get_bar_data(x_field='church', y_field='transferout_count',
                                    data=transfersout_counts, x_title='church', y_title='Number of Transfers out')
        

        

        # Prepare charts list to pass multiple charts
        charts = [
            {'id': 'baptism_json', 'data': json.dumps(baptism_data), 'name': 'baptism', 'total':total_baptism_count},
            {'id': 'transferin_json', 'data': json.dumps(transferin_data), 'name': 'transferin', 'total':total_transfersin},
            {'id': 'transferout_json', 'data': json.dumps(transferout_data), 'name': 'transferout', 'total':total_transfersout},
        ]

        # Render the dashboard with the charts
        context = {
            "charts": charts,
            'year': year,
            'month': month,
            'quarter': quarter,
            'years':years,
            'months': months,
            'quarters': quarters,
        }

        return render(request, 'page/plotly_dashboard.html', context)

plotly_dashboard_charts_page_view = PlotlyDashboardView.as_view()







# class HomepageView1(generic.ListView):
#     template_name = 'root/homepage.html'
#     context_object_name = 'user'
#     login_url = 'login'  # Redirect to login page if not authenticated
    
#     def get_queryset(self):
#         yr = datetime.today().year
#         queryset = { }
         
#         user = self.request.user                      
        
#         # print(self.request.user.username)
#         # print(self.request.user.church) 
#         # print(self.request.user.department) 
#         # print(self.request.user.contact)
#         # print(self.request.user.is_local)  
        
        
#         if user.is_authenticated:
#             if user.is_local:
#                 report_url = reverse("report_dashboard_local")
#             elif user.is_district:
#                 report_url = reverse("report_dashboard_dist")
#             elif user.is_officer:
#                 report_url = reverse("report_dashboard_officer")
#             else:
#                 report_url = "homepage"  # fallback or redirect to unauthorized page
#         else:
#             report_url = reverse("login")

#         context = {
#             "report_url": report_url,
#         }
#         #return render(request, "reports/base_report.html", context)                       
                              
                                      
# homepage_page_view1 = HomepageView1.as_view() 
