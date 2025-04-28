from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Baptism, Dedication, Transfer, Activity, Visitor, Event, Attendance
from .dataFilterClass import ChurchDataExporter, ReportDataExporter, ReportDataExporterDist
from datetime import datetime



MODEL_MAP = {
    "Baptism": (Baptism, "date_baptized"),
    "Transfer": (Transfer, "date_church_voted"),
    "Dedication": (Dedication, "date"),  # example default date field
    # Add more models as needed
}






def get_model_fields(request):
    model_name = request.GET.get('model')
    if model_name not in MODEL_MAP:
        return JsonResponse({'fields': []})

    model_class, _ = MODEL_MAP[model_name]
    fields = [field.name for field in model_class._meta.fields if field.name != 'id']
    return JsonResponse({'fields': fields})



def export_church_data(request):
    if request.method == 'GET' and 'format' in request.GET:
        model_name = request.GET.get('model')
        fields = request.GET.getlist('fields')

        if model_name not in MODEL_MAP or not fields:
            return HttpResponse("Invalid model or fields not selected.", status=400)

        model_class, date_field = MODEL_MAP[model_name]

        church = request.GET.get('church')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        exporter = ChurchDataExporter(model_class, date_field=date_field)
        exporter.filter_data(
            church=church,
            start_date=start_date,
            end_date=end_date
        )

        export_format = request.GET.get('format', 'excel')
        if export_format == 'pdf':
            return exporter.export_to_pdf(fields=fields)
        else:
            return exporter.export_to_excel(fields=fields)

    context = {'model_options': MODEL_MAP.keys()}
    return render(request, 'page/church_data_export.html', context)







MODEL_MAP_local = {
    "Activity": (Activity, "date"),
    "Visitors": (Visitor, "date"),
    # Add more models as needed
}


def get_model_fields_local(request):
    model_name = request.GET.get('model')
    if model_name not in MODEL_MAP_local:
        return JsonResponse({'fields': []})

    model_class, _ = MODEL_MAP_local[model_name]
    fields = [field.name for field in model_class._meta.fields if field.name != 'id']
    return JsonResponse({'fields': fields})


def export_data(request):
    if request.method == 'GET' and 'format' in request.GET:
        model_name = request.GET.get('model')
        fields = request.GET.getlist('fields')

        if model_name not in MODEL_MAP_local or not fields:
            return HttpResponse("Invalid model or fields not selected.", status=400)

        model_class, date_field = MODEL_MAP_local[model_name]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        
        if start_date and end_date:
            # Format month names and handle year
            if start_date.year == end_date.year:
                period = f"{start_date.strftime('%B')} - {end_date.strftime('%B')}, {start_date.year}"
            else:
                period = f"{start_date.strftime('%B %Y')} - {end_date.strftime('%B %Y')}"
        
        exporter = ReportDataExporter(model_class, request, date_field=date_field)
        exporter.filter_data(
            start_date=start_date,
            end_date=end_date
        )

        
        report_info = {
        'period': period,
        'department': request.user.department if hasattr(request.user, 'department') else '',
        'elder': "",
        'leader': "",
        'members':"",
        'reporter':"",
        'church': request.user.church.upper()
    }
        
        
        export_format = request.GET.get('format', 'excel')
        if export_format == 'pdf':
            return exporter.export_to_pdf(fields=fields, report_info=report_info)
        else:
            return exporter.export_to_excel(fields=fields)

    
    context = {'model_options': MODEL_MAP_local.keys()}
    return render(request, 'reports/local/data_export.html', context)







MODEL_MAP_dist = {
    "Baptism": (Baptism, "date_baptized"),
    "Transfer": (Transfer, "date_church_voted"),
    "Dedication": (Dedication, "date"),  # example default date field
    "Activity": (Activity, "date"),
    "Visitors": (Visitor, "date"),
    "Events" : (Event, "date"),
    "Dedication" : (Dedication, "date"),
    "Attendance" : (Attendance, "date"),
    # Add more models as needed
}


def get_model_fields_dist(request):
    model_name = request.GET.get('model')
    if model_name not in MODEL_MAP_dist:
        return JsonResponse({'fields': []})

    model_class, _ = MODEL_MAP_dist[model_name]
    fields = [field.name for field in model_class._meta.fields if field.name != 'id']
    return JsonResponse({'fields': fields})



def export_data_dist(request):
    if request.method == 'GET' and 'format' in request.GET:
        model_name = request.GET.get('model')
        fields = request.GET.getlist('fields')

        if model_name not in MODEL_MAP_dist or not fields:
            return HttpResponse("Invalid model or fields not selected.", status=400)

        model_class, date_field = MODEL_MAP_dist[model_name]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        
        if start_date and end_date:
            # Format month names and handle year
            if start_date.year == end_date.year:
                period = f"{start_date.strftime('%B')} - {end_date.strftime('%B')}, {start_date.year}"
            else:
                period = f"{start_date.strftime('%B %Y')} - {end_date.strftime('%B %Y')}"
        
        exporter = ReportDataExporterDist(model_class, request, date_field=date_field)
        exporter.filter_data(
            start_date=start_date,
            end_date=end_date
        )

        
        report_info = {
        'period': period,
        'church': request.user.church.upper(),
        'report': model_name
    }
        
        
        export_format = request.GET.get('format', 'excel')
        if export_format == 'pdf':
            return exporter.export_to_pdf(fields=fields, report_info=report_info)
        else:
            return exporter.export_to_excel(fields=fields)

    
    context = {'model_options': MODEL_MAP_dist.keys()}
    return render(request, 'reports/district/data_export.html', context)

