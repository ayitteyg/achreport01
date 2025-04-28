from django.db.models import Count, Q, F, Avg, Func
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic import TemplateView
from datetime import datetime
from collections import defaultdict
from .models import Baptism, Transfer, Attendance, Visitor, Event, Dedication, Activity, Department
from .tables import (BaptismSummaryTable, TransferSummaryTable,
                     AttendanceSummaryTable, VisitorMonthlySummaryTable1,
                     EventSummaryTable, DedicationSummaryTable, ActivitySummaryTable)
from .filters import BaptismFilter, TransferFilter, AttendanceFilter, VisitorFilter, EventFilter, DedicationFilter, ActivityFilter
import calendar
import random



from django.db.models import Case, When, IntegerField


class BaptismSummaryView_of(SingleTableMixin, FilterView):
    table_class = BaptismSummaryTable
    template_name = "reports/officer/baptism_report.html"
    filterset_class = BaptismFilter

    def get_queryset(self):
        filter_ = self.filterset_class(self.request.GET, queryset=Baptism.objects.all())
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



class VisitorMonthlySummaryView_of(SingleTableMixin, FilterView):
    table_class = VisitorMonthlySummaryTable1
    template_name = "reports/officer/visitor_report.html"
    filterset_class = VisitorFilter

    def get_queryset(self):
        filter_ = self.filterset_class(self.request.GET, queryset=Visitor.objects.all())
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



class TransferSummaryView_of(SingleTableMixin, FilterView):
    table_class = TransferSummaryTable
    template_name = "reports/officer/transfer_report.html"
    filterset_class = TransferFilter

    def get_queryset(self):
        filter_ = self.filterset_class(self.request.GET, queryset=Transfer.objects.all())
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
    


class AttendanceSummaryView_of(SingleTableMixin, FilterView):
    table_class = AttendanceSummaryTable
    template_name = "reports/officer/attendance_report.html"
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



class EventSummaryView_of(SingleTableMixin, FilterView):
    table_class = EventSummaryTable
    template_name = "reports/officer/event_report.html"
    filterset_class = EventFilter
    model = Event

    def get_queryset(self):
        queryset = super().get_queryset()
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



class DedicationSummaryView_of(SingleTableMixin, FilterView):
    table_class = DedicationSummaryTable
    template_name = "reports/officer/dedication_report.html"
    filterset_class = DedicationFilter
    model = Dedication

    def get_queryset(self):
        queryset = super().get_queryset()
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

        # Optionally, log the summary (use logging instead of print in production)
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.debug(yearly_summary)
        # logger.debug(summary_data)
        
        
        print(yearly_summary)
        print(summary_data)

        return context


    
class ActivitySummaryView_of(SingleTableMixin, FilterView):
    table_class = ActivitySummaryTable
    template_name = "reports/officer/activity_report.html"
    filterset_class = ActivityFilter
    model = Activity

    def get_queryset(self):
        queryset = super().get_queryset()
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
        # print("\n=== DEBUG ===")
        # print(f"Total activities: {qs.count()}")
        # print(f"Selected month: {selected_month}")
        # print(f"Selected dept: {selected_dept}")
        # print(f"Monthly summary: {monthly_summary}")
        # print(f"First month sample: {hierarchical_data[:1]}")

        context.update({
            "filter": self.filter,
            "monthly_summary": monthly_summary,           # <-- Include it here!
            "hierarchical_data": hierarchical_data,
            "selected_month": selected_month,
            "selected_dept": selected_dept,
        })

        return context

