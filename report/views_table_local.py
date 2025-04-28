from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Activity, Visitor
from .tables import (ActivitySummaryTable, VisitorSummaryTable)
from .filters import ActivityFilter, VisitorFilter
import calendar
import random

from django.contrib.auth import get_user_model
User = get_user_model()





    
class ActivitySummaryView_local(SingleTableMixin, FilterView):
    table_class = ActivitySummaryTable
    template_name = "reports/local/activity_report.html"
    filterset_class = ActivityFilter
    model = Activity
    


    def get_queryset(self):
        dept = self.request.user.department
        church = self.request.user.church
        queryset = super().get_queryset()    
        queryset = queryset.filter(department=dept)
        queryset = queryset.filter(church=church)
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        
        # Get department
        dept = self.request.user.department
        
        selected_month = self.request.GET.get("month")

        # Define rating choices mapping
        RATING_CHOICES = {
            1: 'Poor',
            2: 'Fair',
            3: 'Good',
            4: 'Very Good',
            5: 'Excellent',
        }

        # === Monthly Summary ===
        monthly_summary = (
            qs.annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        for m in monthly_summary:
            m["month_name"] = calendar.month_name[m["month"]]

        # === Hierarchical Data ===
        hierarchical_data = []
        for month_data in monthly_summary:
            month = month_data["month"]

            # Get activities for this month and department
            activities = (
                qs.filter(date__month=month)
                .values(
                    "id", "date", "program", "typ", "facilitator",
                    "expense", "income", "rating"
                )
                .order_by("date")
            )

            # Convert activities to list and map rating numbers to descriptions
            activities_list = list(activities)
            for activity in activities_list:
                activity['rating_description'] = RATING_CHOICES.get(activity['rating'], '-')
                # Keep the original rating value as well in case you need it
                activity['rating_value'] = activity['rating']

            # Create department entry with activities
            if dept:
                month_data["departments"] = [{
                    "name": dept,
                    "total": len(activities_list),
                    "activities": activities_list
                }]
            else:
                month_data["departments"] = []

            hierarchical_data.append(month_data)

        context.update({
            "filter": self.filter,
            "monthly_summary": monthly_summary,
            "hierarchical_data": hierarchical_data,
            "selected_month": selected_month,
            "selected_dept": dept,
            "user_dept_name": dept if dept else "No Department",
        })
        
        print(monthly_summary)
        print(Activity.objects.all())
        print(dept)

        return context



class VisitorSummaryView_local(SingleTableMixin, FilterView):
    table_class = VisitorSummaryTable
    template_name = "reports/local/visitor_report.html"
    filterset_class = VisitorFilter
    model = Visitor

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by the user's church
        queryset = queryset.filter(church=self.request.user.church)
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        
        selected_month = self.request.GET.get("month")

        # Monthly Summary
        monthly_summary = (
            qs.annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(
                total_adventist=Count('id', filter=Q(status='adventist')),
                total_non_adventist=Count('id', filter=Q(status='non_adventist'))
            )
            .order_by("month")
        )

        for m in monthly_summary:
            m["month_name"] = calendar.month_name[m["month"]]
            m["total"] = m["total_adventist"] + m["total_non_adventist"]

        # Hierarchical Data
        hierarchical_data = []
        for month_data in monthly_summary:
            month = month_data["month"]

            # Get visitors for this month
            visitors = (
                qs.filter(date__month=month)
                .values("date", "name", "status", "contact")
                .order_by("date")
            )

            month_data["visitors"] = list(visitors)
            hierarchical_data.append(month_data)

        context.update({
            "filter": self.filter,
            "monthly_summary": monthly_summary,
            "hierarchical_data": hierarchical_data,
            "selected_month": selected_month,
            "user_church": self.request.user.church,
        })

        return context