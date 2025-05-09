# baptism/tables.py

import django_tables2 as tables
from django.db.models import Count, Q, F, Func, IntegerField, Value, When, Case
from .models import Baptism, Transfer, Dedication, Activity, Visitor, Treasury
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse

class ExtractYear(Func):
    function = 'EXTRACT'
    template='%(function)s(YEAR FROM %(expressions)s)'

class BaptismSummaryTable(tables.Table):
    year = tables.Column(verbose_name="Year")
    total_baptism = tables.Column(verbose_name="Baptism")
    total_male = tables.Column(verbose_name="Male")
    total_female = tables.Column(verbose_name="Female")
    quarterly_data = tables.Column(empty_values=(), verbose_name="Quarterly Breakdown", orderable=False)
   

    class Meta:
        # attrs = {"class": "table table-striped table-hover"}
        template_name = "django_tables2/bootstrap5.html"  # if using bootstrap5
        attrs = {
            "class": "table table-bordered table-hover table-striped align-middle text-center"
        }



class VisitorMonthlySummaryTable1(tables.Table):
    month = tables.Column(verbose_name="Month")
    total_visitors = tables.Column(verbose_name="Total")
    total_adventist = tables.Column(verbose_name="Adventist")
    total_non_adventist = tables.Column(verbose_name="Non-Adventist")

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-bordered table-hover table-striped align-middle text-center"
        }



class TransferSummaryTable(tables.Table):
    year = tables.Column(verbose_name="Year")
    total_transfers = tables.Column(verbose_name="Total Transfers")
    total_transfers_in = tables.Column(verbose_name="Transfers In")
    total_transfers_out = tables.Column(verbose_name="Transfers Out")
    quarterly_data = tables.Column(
        empty_values=(), 
        verbose_name="Quarterly Breakdown", 
        orderable=False
    )

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-bordered table-hover table-striped align-middle text-center"
        }

    @staticmethod
    def get_queryset():
        return Transfer.objects.annotate(
            year=ExtractYear('date_church_voted')
        ).values('year').annotate(
            total_transfers=Count('id'),
            total_transfers_in=Count(
                Case(
                    When(typ='transfer_in', then=1),
                    output_field=IntegerField()
                )
            ),
            total_transfers_out=Count(
                Case(
                    When(typ='transfer_out', then=1),
                    output_field=IntegerField()
                )
            )
        ).order_by('-year')
    



class AttendanceSummaryTable(tables.Table):
    month = tables.Column(verbose_name="Month")
    avg_adults = tables.Column(verbose_name="Avg Adults")
    avg_youth = tables.Column(verbose_name="Avg Youth") 
    avg_children = tables.Column(verbose_name="Avg Children")
    monthly_data = tables.Column(
        empty_values=(),
        verbose_name="Weekly Breakdown",
        orderable=False
    )

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-bordered table-hover table-striped align-middle text-center"
        }



class EventSummaryTable(tables.Table):
    date = tables.Column(verbose_name="Date", visible=False)
    event_type = tables.Column(verbose_name="Event Type")
    member_involved = tables.Column(verbose_name="Member Involved", visible=False)
    total = tables.Column(verbose_name="Total", visible=False)

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-bordered text-center"}



class DedicationSummaryTable(tables.Table):
    child_name = tables.Column(verbose_name="Child Name")
    date = tables.DateColumn(verbose_name="Date", format="Y-m-d", visible=False)
    total = tables.Column(verbose_name="Count", visible=False)

    # Optional: hidden data for detail toggle
    mother_name = tables.Column(verbose_name="Mother", visible=False)
    father_name = tables.Column(verbose_name="Father", visible=False)
    date_of_birth = tables.DateColumn(verbose_name="DOB", format="Y-m-d", visible=False)
    place_of_birth = tables.Column(verbose_name="Place", visible=False)

    class Meta:
        model = Dedication
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-bordered text-start"}
        


class ActivitySummaryTable(tables.Table):
    month = tables.Column(verbose_name="Month")
    total = tables.Column(verbose_name="Total Programs")
    action = tables.Column(empty_values=(), orderable=False)

    def render_action(self, record):
        return format_html(
            '<a href="?month={}">View Departments</a>',
            record['month']
        )

    class Meta:
        model = Activity
        fields = ()




class VisitorSummaryTable(tables.Table):
    month = tables.Column(verbose_name="Month")
    total_adventist = tables.Column(verbose_name="Adventist")
    total_non_adventist = tables.Column(verbose_name="Non-Adventist")
    total_visitors = tables.Column(verbose_name="Total Visitors")
    detail = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    def render_total_visitors(self, value, record):
        return record['total_adventist'] + record['total_non_adventist']

    def render_action(self, record):
        return format_html(
            '<a href="?month={}" class="btn btn-sm btn-info">View Visitors</a>',
            record['month']
        )

    class Meta:
        attrs = {
            'class': 'table table-bordered table-hover',
            'thead': {
                'class': 'thead-light'
            }
        }


class TreasurySummaryTable(tables.Table):
    month = tables.Column(verbose_name='Month')
    returns = tables.Column(verbose_name='Total Returns (₵)')
    other_receipts = tables.Column(verbose_name='Other Receipts (₵)')
    payments = tables.Column(verbose_name='Payments (₵)')
    details = tables.Column(verbose_name='Actions', empty_values=(), orderable=False)

    class Meta:
        attrs = {
            'class': 'table table-striped table-bordered',
            'thead': {
                'class': 'table-light'
            }
        }

    def render_returns(self, value):
        return f"{value:,.2f}"

    def render_other_receipts(self, value):
        return f"{value:,.2f}"

    def render_payments(self, value):
        return f"{value:,.2f}"
    
    
    
    def render_detail(self, record):
        return format_html(
            '<a href="?month={}" class="btn btn-sm btn-info">View Detail</a>',
            record['month']
        )




# class TreasurySummaryTable(tables.Table):
#     month = tables.Column(verbose_name='Month')
#     returns = tables.Column(verbose_name='Total Returns (₵)')
#     other_receipts = tables.Column(verbose_name='Other Receipts (₵)')
#     payments = tables.Column(verbose_name='Payments (₵)')
#     details = tables.Column(verbose_name='Actions', empty_values=(), orderable=False)

#     class Meta:
#         attrs = {
#             'class': 'table table-striped table-bordered',
#             'thead': {
#                 'class': 'table-light'
#             }
#         }
#         # fields = ('month', 'returns', 'other_receipts', 'payments', 'details')
#         # order_by = ('-year', '-month')

#     def render_returns(self, value):
#         return f"{value:,.2f}"

#     def render_other_receipts(self, value):
#         return f"{value:,.2f}"

#     def render_payments(self, value):
#         return f"{value:,.2f}"

#     def render_details(self, record):
#         return format_html(
#             '<button class="btn btn-sm btn-outline-primary toggle-month" data-month="{}-{}">'
#             '<i class="bi bi-caret-down"></i> Details'
#             '</button>',
#             # record['month'], record['year']
#         )
        
   