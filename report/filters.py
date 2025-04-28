# report/filters.py

import django_filters
from .models import Baptism, Transfer, Attendance, Visitor, Event, Dedication, Activity, Department
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek






class BaptismFilter(django_filters.FilterSet):
    church = django_filters.ChoiceFilter(
        choices=[('', 'All')] + list(Baptism._meta.get_field('church').choices),
        label='Church'
    )

    class Meta:
        model = Baptism
        fields = ['church']




class VisitorFilter0(django_filters.FilterSet):
    church = django_filters.ChoiceFilter(
        choices=[('', 'All')] + list(Visitor._meta.get_field('church').choices),
        label='Church'
    )

    year = django_filters.ChoiceFilter(
        label='Year',
        method='filter_by_year'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Dynamically populate year choices from existing Visitor records
        years = (
            Visitor.objects.annotate(year=ExtractYear('date'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
        )

        self.filters['year'].field.choices = [('', 'All')] + [(y, y) for y in years if y]

    def filter_by_year(self, queryset, name, value):
        if value:
            return queryset.filter(date__year=value)
        return queryset

    class Meta:
        model = Visitor
        fields = ['church', 'year']



class TransferFilter(django_filters.FilterSet):
    church = django_filters.ChoiceFilter(
        choices=[('', 'All')] + list(Transfer._meta.get_field('church').choices),
        label='Current Church'
    )
    
    status = django_filters.ChoiceFilter(
        choices=[('', 'All')] + list(Transfer._meta.get_field('status').choices),
        label='Transfer Status'
    )

    class Meta:
        model = Transfer
        fields = ['church', 'status']




class AttendanceFilter(django_filters.FilterSet):
    # Church filter (exact match from your CHURCH choices)
    church = django_filters.ChoiceFilter(
        field_name='church',
        lookup_expr='iexact',
        label='Church',
        choices=Attendance.church  # Uses your model's CHURCH choices
    )
    
    # Year filter (dynamically populated from existing data)
    year = django_filters.ChoiceFilter(
        field_name='date',
        lookup_expr='year',
        label='Year',
        choices=[]  # Populated in __init__
    )

    class Meta:
        model = Attendance
        fields = ['church', 'year']  # Only these two filters

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically set year choices from existing data
        years = Attendance.objects.annotate(
            year=ExtractYear('date')
        ).values_list('year', flat=True).distinct().order_by('-year')
        
        self.filters['year'].extra['choices'] = [(y, y) for y in years]
    church = django_filters.ChoiceFilter(
        choices=[('', 'All Churches')] + list(Attendance._meta.get_field('church').choices),
        label='Church',
       
    )
    
    year = django_filters.NumberFilter(
        method='filter_by_year',
        label='Year',
    )

    class Meta:
        model = Attendance
        fields = ['church', 'year']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get unique years from the database
        years = (
            Attendance.objects
            .annotate(year=ExtractYear('date'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')  # Sort descending (newest first)
        )
        
        # Update the 'year' field to use a ChoiceFilter with dynamic choices
        self.filters['year'] = django_filters.ChoiceFilter(
            field_name='date',
            lookup_expr='year',
            choices=[(year, year) for year in years],
            label='Year',
        )

    def filter_by_year(self, queryset, name, value):
        return queryset.filter(date__year=value)
    
    



class EventFilter(django_filters.FilterSet):
    church = django_filters.ChoiceFilter(
        field_name='church',
        choices=[('', 'All Churches')] + list(Event._meta.get_field('church').choices),
        label='Church',
    )

    year = django_filters.ChoiceFilter(
        field_name='date',
        lookup_expr='year',
        label='Year',
        choices=[]
    )

    class Meta:
        model = Event
        fields = ['church', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = (
            Event.objects.annotate(year=ExtractYear('date'))
            .values_list('year', flat=True).distinct().order_by('-year')
        )
        self.filters['year'].extra['choices'] = [(y, y) for y in years]




class DedicationFilter(django_filters.FilterSet):
    church = django_filters.ChoiceFilter(
        field_name='church',
        choices=[('', 'All Churches')] + list(Dedication._meta.get_field('church').choices),
        label='Church',
    )

    year = django_filters.ChoiceFilter(
        field_name='date',
        lookup_expr='year',
        label='Year',
        choices=[]
    )

    class Meta:
        model = Dedication
        fields = ['church', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = (
            Dedication.objects.annotate(year=ExtractYear('date'))
            .values_list('year', flat=True).distinct().order_by('-year')
        )
        self.filters['year'].extra['choices'] = [(y, y) for y in years]






class ActivityFilter(django_filters.FilterSet):
    church = django_filters.ChoiceFilter(
        field_name='church',
        choices=[('', 'All Churches')] + list(Activity._meta.get_field('church').choices),
        label='Church',
    )

    department = django_filters.ModelChoiceFilter(
        field_name='department',
        queryset=Department.objects.all(),
        label='Department',
        empty_label='All Departments',
    )

    year = django_filters.ChoiceFilter(
        field_name='date',
        lookup_expr='year',
        label='Year',
        choices=[],
    )

    class Meta:
        model = Activity
        fields = ['church', 'department', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = (
            Activity.objects.annotate(year=ExtractYear('date'))
            .values_list('year', flat=True).distinct().order_by('-year')
        )
        self.filters['year'].extra['choices'] = [(y, y) for y in years]
        
        
        
 
class VisitorFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(
        field_name='date',
        lookup_expr='year',
        label='Year',
        choices=[],
        
    )

    class Meta:
        model = Visitor
        fields = ['year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get distinct years from Visitor data, ordered descending
        years = (
            Visitor.objects.annotate(year=ExtractYear('date'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
        )
        
        # Update the choices for the year filter
        self.filters['year'].extra['choices'] = [(y, y) for y in years]
        
        # Get distinct churches for the church filter
        #churches = Visitor.objects.values_list('church', flat=True).distinct()
        #self.filters['church'].field.queryset = churches