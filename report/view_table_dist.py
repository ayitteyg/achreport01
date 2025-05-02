from django.db.models import Count, Q, Func, Avg, Min, Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractWeek, TruncWeek
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Activity, Visitor, Baptism, Transfer, Attendance, Dedication, Event
from .tables import (ActivitySummaryTable, VisitorSummaryTable, 
                     BaptismSummaryTable, TransferSummaryTable, AttendanceSummaryTable,
                     DedicationSummaryTable, EventSummaryTable)
from .filters import ActivityFilter, VisitorFilter, BaptismFilter, TransferFilter, AttendanceFilter, DedicationFilter, EventFilter
import calendar
from collections import defaultdict
from django.db.models import Case, When, IntegerField
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()




class BaptismSummaryView_dist(SingleTableMixin, FilterView):
    table_class = BaptismSummaryTable
    template_name = "reports/district/baptism_report.html"
    filterset_class = BaptismFilter

    
    def get_queryset(self):
        church = self.request.user.church
        filter_ = self.filterset_class(self.request.GET, queryset=Baptism.objects.all().filter(church=church))
        return filter_.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = self.get_queryset().annotate(
            year_=ExtractYear('date_baptized'),
            month=ExtractMonth('date_baptized')
        )

        # Yearly Summary
        yearly_data = qs.values('year_').annotate(
            total_baptism=Count('id'),
            total_male=Count('id', filter=Q(gender='M')),
            total_female=Count('id', filter=Q(gender='F'))
        ).order_by('year_')

        # Quarterly Data within Year
        quarterly_data = qs.annotate(
            quarter=Case(
                When(month__in=[1, 2, 3], then=1),
                When(month__in=[4, 5, 6], then=2),
                When(month__in=[7, 8, 9], then=3),
                When(month__in=[10, 11, 12], then=4),
                output_field=IntegerField()
            )
        ).values('year_', 'quarter').annotate(
            total=Count('id'),
            male=Count('id', filter=Q(gender='M')),
            female=Count('id', filter=Q(gender='F')),
        ).order_by('year_', 'quarter')

        # Group Quarterly Data under year
        quarterly_summary = {}
        for q in quarterly_data:
            year = q['year_']
            quarter = {
                'quarter': f"Q{q['quarter']}",
                'total': q['total'],
                'male': q['male'],
                'female': q['female']
            }
            quarterly_summary.setdefault(year, []).append(quarter)

        context['yearly_data'] = yearly_data
        context['quarterly_data'] = quarterly_summary
        
        #print(quarterly_summary)
        return context



class TransferSummaryView_dist(SingleTableMixin, FilterView):
    table_class = TransferSummaryTable
    template_name = "reports/district/transfer_report.html"
    filterset_class = TransferFilter

    def get_queryset(self):
        church = self.request.user.church
        status = 'complete'
        filter_ = self.filterset_class(self.request.GET, queryset=Transfer.objects.all().filter(church=church, status=status))
        return filter_.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = self.get_queryset().annotate(
            year_=ExtractYear('date_church_voted'),
            month=ExtractMonth('date_church_voted')
        )

        # Yearly Summary
        yearly_data = qs.values('year_').annotate(
            total_transfers=Count('id'),
            total_transfers_in=Count('id', filter=Q(typ='transfer_in')),
            total_transfers_out=Count('id', filter=Q(typ='transfer_out'))
        ).order_by('year_')

        # Quarterly Data within Year
        quarterly_data = qs.annotate(
            quarter=Case(
                When(month__in=[1, 2, 3], then=1),
                When(month__in=[4, 5, 6], then=2),
                When(month__in=[7, 8, 9], then=3),
                When(month__in=[10, 11, 12], then=4),
                output_field=IntegerField()
            )
        ).values('year_', 'quarter').annotate(
            total=Count('id'),
            transfers_in=Count('id', filter=Q(typ='transfer_in')),
            transfers_out=Count('id', filter=Q(typ='transfer_out'))
        ).order_by('year_', 'quarter')

        # Group Quarterly Data under year
        quarterly_summary = {}
        for q in quarterly_data:
            year = q['year_']
            quarter = {
                'quarter': f"Q{q['quarter']}",
                'total': q['total'],
                'transfers_in': q['transfers_in'],
                'transfers_out': q['transfers_out']
            }
            quarterly_summary.setdefault(year, []).append(quarter)

        context['yearly_data'] = yearly_data
        context['quarterly_data'] = quarterly_summary
        return context
    

class AttendanceSummaryView_dist(SingleTableMixin, FilterView):
    table_class = AttendanceSummaryTable
    template_name = "reports/district/attendance_report.html"
    filterset_class = AttendanceFilter
    model = Attendance

    def get_queryset(self):
        church = self.request.user.church
        queryset = super().get_queryset().filter(church=church).annotate(
            month=ExtractMonth('date'),
            year=ExtractYear('date')
        )
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()

        # Monthly Totals
        monthly_totals = (
            filtered_qs
            .values('year', 'month')
            .annotate(
                avg_adults=Func(Avg('adult'), function='CEIL'),
                avg_youth=Func(Avg('youth'), function='CEIL'),
                avg_children=Func(Avg('children'), function='CEIL'),
                first_date=Min('date')
            )
            .order_by('year', 'month')
        )

        # Service-wise Monthly Averages
        service_avgs = (
            filtered_qs
            .values('year', 'month', 'service')
            .annotate(
                service_avg_adults=Func(Avg('adult'), function='CEIL'),
                service_avg_youth=Func(Avg('youth'), function='CEIL'),
                service_avg_children=Func(Avg('children'), function='CEIL'),
                first_date=Min('date')
            )
            .order_by('year', 'month', 'service')
        )

        # Organize data by month
        organized_data = []
        for month in monthly_totals:
            month_entry = {
                'year': month['year'],
                'month': month['month'],
                'month_name': month['first_date'].strftime('%B %Y'),
                'month_year': f"{month['month']}-{month['year']}",
                'totals': {
                    'adults': month['avg_adults'],
                    'youth': month['avg_youth'],
                    'children': month['avg_children']
                },
                'services': []
            }
            
            # Add service averages for this month
            for service in service_avgs:
                if (service['year'] == month['year'] and 
                    service['month'] == month['month']):
                    month_entry['services'].append({
                        'name': service['service'],
                        'adults': service['service_avg_adults'],
                        'youth': service['service_avg_youth'],
                        'children': service['service_avg_children']
                    })
            
            organized_data.append(month_entry)  # Moved this line to the end

        context.update({
            'attendance_data': organized_data,
            'current_month': int(self.request.GET.get('month', datetime.now().month)),
            'current_year': int(self.request.GET.get('year', datetime.now().year))
        })
        
        #print(organized_data    )
        return context


class AttendanceSummaryView_dist2(SingleTableMixin, FilterView):
    table_class = AttendanceSummaryTable
    template_name = "reports/district/attendance_report.html"
    filterset_class = AttendanceFilter
    model = Attendance

    def get_queryset(self):
        church =  self.request.user.church
        queryset = super().get_queryset().filter(church=church).annotate(
            month=ExtractMonth('date')
        )
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()

        # Monthly Data
        monthly_data = (
            filtered_qs
            .values('month')
            .annotate(
                avg_adults=Func(Avg('adult'), function='CEIL'),
                avg_youth=Func(Avg('youth'), function='CEIL'),
                avg_children=Func(Avg('children'), function='CEIL')
            )
            .order_by('month')
        )

        # Add month names
        for m in monthly_data:
            m['month_name'] = calendar.month_name[m['month']]

        # Weekly Data
        weekly_data = defaultdict(list)
        if 'month' in self.request.GET:
            selected_month = int(self.request.GET['month'])
            weekly_entries = (
                filtered_qs
                .filter(date__month=selected_month)
                .annotate(week=ExtractWeek('date'))
                .order_by('week', 'date')
            )

            for entry in weekly_entries:
                weekly_data[entry.week].append({
                    'date': entry.date,
                    'adults': entry.adult,
                    'youth': entry.youth,
                    'children': entry.children,
                })

        context['monthly_data'] = monthly_data
        context['weekly_data'] = dict(weekly_data)  # Convert to normal dict
        
        print(monthly_data)
        print(weekly_data)
        
        return context




class AttendanceSummaryView(SingleTableMixin, FilterView):
    table_class = AttendanceSummaryTable
    template_name = "reports/attendance_report.html"
    filterset_class = AttendanceFilter
    model = Attendance

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            month=ExtractMonth('date')
        )
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()

        # Monthly Data
        monthly_data = (
            filtered_qs
            .values('month')
            .annotate(
                avg_adults=Func(Avg('adult'), function='CEIL'),
                avg_youth=Func(Avg('youth'), function='CEIL'),
                avg_children=Func(Avg('children'), function='CEIL')
            )
            .order_by('month')
        )

        # Add month names
        for m in monthly_data:
            m['month_name'] = calendar.month_name[m['month']]

        # Weekly Data
        weekly_data = defaultdict(list)
        if 'month' in self.request.GET:
            selected_month = int(self.request.GET['month'])
            weekly_entries = (
                filtered_qs
                .filter(date__month=selected_month)
                .annotate(week=ExtractWeek('date'))
                .order_by('week', 'date')
            )

            for entry in weekly_entries:
                weekly_data[entry.week].append({
                    'date': entry.date,
                    'adults': entry.adult,
                    'youth': entry.youth,
                    'children': entry.children,
                })

        context['monthly_data'] = monthly_data
        context['weekly_data'] = dict(weekly_data)  # Convert to normal dict
        return context




class DedicationSummaryView_dist(SingleTableMixin, FilterView):
    table_class = DedicationSummaryTable
    template_name = "reports/district/dedication_report.html"
    filterset_class = DedicationFilter
    model = Dedication

    def get_queryset(self):
        church = self.request.user.church
        queryset = super().get_queryset().filter(church=church)
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()

        # Yearly count summary
        yearly_summary = (
            filtered_qs
            .annotate(year=ExtractYear('date'))
            .values('year')
            .annotate(total=Count('id'))
            .order_by('-year')
        )

        # Detailed summary
        summary_data = filtered_qs.values(
            'child_name', 'date', 'mother_name',
            'father_name', 'date_of_birth', 'place_of_birth'
        ).order_by('-date')

        context['yearly_summary'] = yearly_summary
        context['summary_data'] = summary_data
        context['filter'] = self.filter 
        
        # print(yearly_summary)
        # print(summary_data)

        return context



class VisitorMonthlySummaryView_dist(SingleTableMixin, FilterView):
    table_class = VisitorSummaryTable
    template_name = "reports/district/visitor_report.html"
    filterset_class = VisitorFilter

    def get_queryset(self):
        church = self.request.user.church
        filter_ = self.filterset_class(self.request.GET, queryset=Visitor.objects.all().filter(church=church))
        self.filtered_qs = filter_.qs
        return self.filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = self.get_queryset().annotate(
            month=ExtractMonth('date')
        )

        # Group by month
        monthly_data = (
            qs.values('month')
            .annotate(
                total_visitors=Count('id'),
                total_adventist=Count('id', filter=Q(status="adventist")),
                total_non_adventist=Count('id', filter=Q(status="non_adventist"))
            )
            .order_by('month')
        )

        # Add month name for display
        for m in monthly_data:
            m['month'] = calendar.month_name[m['month']]

        context['monthly_data'] = monthly_data
        return context




class EventSummaryView_dist(SingleTableMixin, FilterView):
    table_class = EventSummaryTable
    template_name = "reports/district/event_report.html"
    filterset_class = EventFilter
    model = Event

    def get_queryset(self):
        church=self.request.user.church
        queryset = super().get_queryset().filter(church=church)
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()

        # Summary data
        summary_data = (
            filtered_qs
            .values('event_type')
            .annotate(total=Count('event_type'))
            .order_by('event_type')
        )

        # Detail data
        detail_data = filtered_qs.values('date', 'event_type', 'member_involved')

        # Pass summary_data and detail_data to the context
        context['summary_data'] = summary_data
        context['detail_data'] = detail_data
        context['filter'] = self.filter

      
        # print("Summary Data:", summary_data)
        # print("Detail Data:", detail_data)
        
        return context




class VisitorSummaryView_dist(SingleTableMixin, FilterView):
    table_class = VisitorSummaryTable
    template_name = "reports/district/visitor_report.html"
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
    


    
class ActivitySummaryView_dist(SingleTableMixin, FilterView):
    table_class = ActivitySummaryTable
    template_name = "reports/district/activity_report.html"
    filterset_class = ActivityFilter
    model = Activity

    def get_queryset(self):
        church = self.request.user.church
        queryset = super().get_queryset().filter(church=church)
        self.filter = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        selected_month = self.request.GET.get("month")
        selected_dept = self.request.GET.get("dept")

        # === Monthly Summary (simple) ===
        monthly_summary = (
            qs.annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        for m in monthly_summary:
            m["month_name"] = calendar.month_name[m["month"]]

        # === Full Hierarchical Data (month > departments > activities for all) ===
        hierarchical_data = []
        for month_data in monthly_summary:
            month = month_data["month"]

            # Get department summary for this month
            dept_summary = (
                qs.filter(date__month=month)
                .values("department")
                .annotate(total=Count("id"))
                .order_by("department")
            )

            month_data["departments"] = []
            for dept in dept_summary:
                dept_data = {
                    "name": dept["department"],
                    "total": dept["total"],
                    "activities": []
                }

                # Always include activities for each department in the month
                activities = (
                    qs.filter(date__month=month, department=dept["department"])
                    .values(
                        "id", "date", "program", "typ", "facilitator",
                        "expense", "income", "rating"
                    )
                    .order_by("date")
                )
                dept_data["activities"] = list(activities)

                month_data["departments"].append(dept_data)

            hierarchical_data.append(month_data)

        # === Debugging Info ===
        print("\n=== DEBUG ===")
        print(f"Total activities: {qs.count()}")
        print(f"Selected month: {selected_month}")
        print(f"Selected dept: {selected_dept}")
        print(f"Monthly summary: {monthly_summary}")
        print(f"First month sample: {hierarchical_data[:1]}")

        context.update({
            "filter": self.filter,
            "monthly_summary": monthly_summary,           # <-- Include it here!
            "hierarchical_data": hierarchical_data,
            "selected_month": selected_month,
            "selected_dept": selected_dept,
        })

        return context

